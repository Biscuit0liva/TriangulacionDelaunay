import pyglet
from OpenGL import GL
import numpy as np
import os
from pathlib import Path
import random
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
    mode = argv[1]
    if mode == "u":         # grilla uniforme
        rows = int(argv[2])
        cols = int(argv[3])
    elif mode == "ur":      # grilla uniforme eligiendo puntos aleatorios
        rows = int(argv[2])
        cols = int(argv[3])
        n = int(argv[4])
    elif mode == "r":       # puntos aleatorios, en un rango de (-a,a) x (-b,b)
        a = int(argv[2])
        b = int(argv[3])    
        n = int(argv[4])
    elif mode == "c":       # puntos aleatorios, en un rango circular
        radio = int(argv[2])
        n = int(argv[3])
    else:
        print("Modo no valido")
        exit()
except:
    print("faltan argumentos")
    exit()

if __name__ == "__main__":
    width = 700
    height = 700
    win = pyglet.window.Window(
        width, height, "Visualizador de archivos m2d", resizable=False
    )
    T = Triangulation(1e-10)
    puntos = []
    # grilla de puntos
    if mode == "u":
        for i in range(rows):
            for j in range (cols):
                puntos.append(point(i,j))
    # grilla de puntos con puntos aleatorios
    elif mode == "ur":
        for i in range(rows):
            for j in range (cols):
                puntos.append(point(i,j))
        if n > len(puntos):
            print("n mayor a la cantidad de puntos")
            exit()
        puntos = random.sample(puntos, n)
    # puntos aleatorios en un rango rectangular
    elif mode == "r":
        for _ in range(n):
            x = random.uniform(-a,a)
            y = random.uniform(-b,b)
            puntos.append(point(x,y))
    # puntos aleatorios en un rango circular
    elif mode == "c":
        for _ in range(n):
            r = radio*np.sqrt(random.uniform(0,1))
            theta = random.uniform(0,2*np.pi)
            x = r*np.cos(theta)
            y = r*np.sin(theta)
            puntos.append(point(x,y))
    else:
        print("Modo no valido")
        exit()
    
    
    

    T.triangulate(puntos)

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
