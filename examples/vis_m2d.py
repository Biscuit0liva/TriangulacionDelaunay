import pyglet
from OpenGL import GL
import numpy as np
import os
from pathlib import Path

from sys import argv
import sys
# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from point import point
from Triangle import Triangle
from Triangulation import Triangulation
from algorithms.load import read_triangulation


def translate(tx, ty, tz):
    return np.array(
        [[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]], dtype=np.float32
    )


def uniformScale(s):
    return np.array(
        [[s, 0, 0, 0], [0, s, 0, 0], [0, 0, s, 0], [0, 0, 0, 1]], dtype=np.float32
    )


# A class to store the application control
class Controller:
    x = 0.0
    y = 0.0
    vx = 0.0
    vy = 0.0


controller = Controller()

path_to_this_file = Path(os.path.dirname(__file__))

try:
    m2d_file = argv[1]
except:
    print("file not specified")
    exit()

if __name__ == "__main__":
    width = 700
    height = 700
    win = pyglet.window.Window(
        width, height, "Visualizador de archivos m2d", resizable=False
    )
    T = Triangulation(1e-10)
    # puntos
    a = point(0, 0)    # 0
    b = point(1, -1)   # 1  
    c = point(1, 1)    # 2
    d = point(2, 0)    # 3
    e = point(2, 1)    # 4
    f = point(-1, 1)   # 5
    g = point(0, -2)   # 6
    h = point(3, -2)   # 7
    T.points = [a, b, c, d, e, f, g, h]
    T.cnt = 8

     # triangulos de prueba
    t1 = Triangle(0, 1, 2)
    t2 = Triangle(2, 1, 3)
    t3 = Triangle(3, 4, 2)
    t4 = Triangle(5, 0, 2)
    t5 = Triangle(1, 0, 6)
    t6 = Triangle(7, 3, 1)

    # seteamos sus vecinos
    t1.set_vecino(0, t2)
    t1.set_vecino(1, t4)
    t1.set_vecino(2, t5)
    t2.set_vecino(0, t6)
    t2.set_vecino(1, t3)
    t2.set_vecino(2, t1)
    t3.set_vecino(1, t2)
    t4.set_vecino(0, t1)
    t5.set_vecino(2, t1)
    t6.set_vecino(0, t2)
    # agregamos los triangulos a la triangulación
    T.triangles.append(t1)
    T.triangles.append(t6)
    T.triangles.append(t5)
    T.triangles.append(t4)
    T.triangles.append(t3)
    T.triangles.append(t2)
    # insertamos un punto en t1
    p1 = point(0.3,-0.1)
    T.insert3(T.triangles[0], p1)
    T.legalize_edge(T.triangles[6], T.triangles[5])
    T.legalize_edge(T.triangles[0], T.triangles[2])
    T.legalize_edge(T.triangles[7], T.triangles[3])

    vertices, indices, min_x, min_y, max_x, max_y = read_triangulation(T)

    range_x = abs(max_x - min_x)
    range_y = abs(max_y - min_y)
    zoom = max([range_x, range_y]) / 2

    controller.zoom = 0.8 / zoom
    controller.x = 1 - range_x / zoom
    controller.y = 1 - range_y / zoom

    with open(path_to_this_file / "../shaders/simple_vertex_program.glsl") as f:
        vertex_source_code = f.read()

    with open(path_to_this_file / "../shaders/dummy_fragment_program.glsl") as f:
        fragment_source_code = f.read()

    vert_shader = pyglet.graphics.shader.Shader(vertex_source_code, "vertex")
    frag_shader = pyglet.graphics.shader.Shader(fragment_source_code, "fragment")
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_shader, frag_shader)

    gpu_data = pipeline.vertex_list_indexed(
        len(vertices) // 3, GL.GL_TRIANGLES, indices
    )
    gpu_data.position[:] = vertices
    gpu_data.color[:] = np.full(len(vertices), 0.5)

    pipeline.use()

    @win.event
    def on_key_press(key, mod):
        if key == pyglet.window.key.UP:
            if mod & pyglet.window.key.MOD_CTRL:
                controller.zoom *= 1.2
            else:
                controller.vy = 0.005
        elif key == pyglet.window.key.DOWN:
            if mod & pyglet.window.key.MOD_CTRL:
                controller.zoom /= 1.2
            else:
                controller.vy = -0.005
        elif key == pyglet.window.key.LEFT:
            controller.vx = -0.005
        elif key == pyglet.window.key.RIGHT:
            controller.vx = 0.005

    @win.event
    def on_key_release(key, mod):
        if key == pyglet.window.key.UP:
            controller.vy = 0
        elif key == pyglet.window.key.DOWN:
            controller.vy = 0
        elif key == pyglet.window.key.LEFT:
            controller.vx = 0
        elif key == pyglet.window.key.RIGHT:
            controller.vx = 0

    from pyglet.window import mouse

    @win.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            controller.x += 2 * dx / width
            controller.y += 2 * dy / height

    @win.event
    def on_draw():
        GL.glClearColor(0.0, 0.0, 0.0, 1.0)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        GL.glPointSize(5)

        win.clear()
        pipeline.use()

        pipeline["translate"] = translate(controller.x, controller.y, 0.0).reshape(
            16, 1, order="F"
        )
        pipeline["scale"] = uniformScale(controller.zoom).reshape(16, 1, order="F")

        gpu_data.draw(GL.GL_TRIANGLES)

    def update(time):
        controller.x += controller.vx
        controller.y += controller.vy

    pyglet.clock.schedule_interval(update, 1 / 60)

    pyglet.app.run()
