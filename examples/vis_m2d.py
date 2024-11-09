import pyglet
from OpenGL import GL
import numpy as np
import os
from pathlib import Path
import random
from sys import argv
import sys
import time
import re
# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from point import point
from Edge import Edge
from Triangle import Triangle
from Triangulation import Triangulation
from algorithms.load import read_triangulation


# indice del triangulo actual para mostrar su LEPP
current_triangle_index = 0

def update_lepp_visualization():
    global gpu_green_edges
    # Obtener el triángulo actual y calcular su LEPP
    current_triangle = T.triangles[current_triangle_index]
    lepp_triangles = T.find_lepp(current_triangle)

    # Preparar la lista de aristas en verde para el camino LEPP
    green_edges = []
    for triangle in lepp_triangles:
        for i in range(3):
            i1, i2 = triangle.get_arista_opuesta(i)
            v1 = T.points[i1]
            v2 = T.points[i2]
            green_edges.extend([v1.x, v1.y, 0, v2.x, v2.y, 0])

    # Cargar las aristas del LEPP en GPU con color verde
    green_edge_colors = np.array([0.0, 1.0, 0.0] * (len(green_edges) // 3), dtype=np.float32)  # Verde

    if gpu_green_edges:
        gpu_green_edges.delete()  # Eliminar la lista anterior

    gpu_green_edges = pipeline.vertex_list(
        len(green_edges) // 3, GL.GL_LINES,
    )
    gpu_green_edges.position[:] = green_edges
    gpu_green_edges.color[:] = green_edge_colors

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
    
    # arista restringida
    elif mode == "er":
        a = int(argv[2])
        b = int(argv[3])    
        n = int(argv[4])
        edges = []
        for i in range(5,len(argv)):
            try:
                edge = eval(argv[i])
                if (isinstance(edge, tuple) and len(edge) == 2 and
                    all(isinstance(point,tuple) and len(point)==2 for point in edge)):
                    edges.append(edge)
                else:
                    raise ValueError(f"Formato de arista inválido: {sys.argv[i]}")
            except:
                print(f"Error: El argumento {sys.argv[i]} no es una arista válida.")
                sys.exit(1)
    # arista restringida aleatoria
    elif mode == "err":
        a = int(argv[2])
        b = int(argv[3])    
        n = int(argv[4])
        edges = []
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
    puntos = []
    aristas = None
    # grilla de puntos
    if mode == "u":
        for i in range(rows):
            for j in range (cols):
                puntos.append(point(i,j))
        minx = 0
        miny = 0
        maxx = rows
        maxy = cols
    # grilla de puntos con puntos aleatorios
    elif mode == "ur":
        for i in range(rows):
            for j in range (cols):
                puntos.append(point(i,j))
        if n > len(puntos):
            print("n mayor a la cantidad de puntos")
            exit()
        puntos = random.sample(puntos, n)
        minx = 0
        miny = 0
        maxx = rows
        maxy = cols
    # puntos aleatorios en un rango rectangular
    elif mode == "r":
        for _ in range(n):
            x = random.uniform(-a,a)
            y = random.uniform(-b,b)
            puntos.append(point(x,y))
        minx = -a
        miny = -b
        maxx = a
        maxy = b
    # puntos aleatorios en un rango circular
    elif mode == "c":
        for _ in range(n):
            r = radio*np.sqrt(random.uniform(0,1))
            theta = random.uniform(0,2*np.pi)
            x = r*np.cos(theta)
            y = r*np.sin(theta)
            puntos.append(point(x,y))
        minx = -r
        miny = -r
        maxx = r
        maxy = r
    # arista restringida
    # puntos aleatorios en un rango rectangular
    elif mode == "er":
        for _ in range(n):
            x = random.uniform(-a,a)
            y = random.uniform(-b,b)
            puntos.append(point(x,y))
        minx = -a
        miny = -b
        maxx = a
        maxy = b
        aristas = []
        for e in edges:
            p1 = point(e[0][0],e[0][1])
            p2 = point(e[1][0],e[1][1])
            aristas.append(Edge(p1,p2))
    # arista restringida aleatoria, toma 2 puntos aleatorios y los usa como arista restringida
    elif mode == "err":
        for _ in range(n):
            x = random.uniform(-a,a)
            y = random.uniform(-b,b)
            puntos.append(point(x,y))
        minx = -a
        miny = -b
        maxx = a
        maxy = b
        aristas = []
        p1 = random.choice(puntos)
        p2 = random.choice(puntos)
        aristas.append(Edge(p1,p2))
    else:
        print("Modo no valido")
        exit()
    
    # creo la triangulacion y triangulo los puntos
    T = Triangulation(minx, maxx, miny, maxy, 1e-10)
    # tomo el tiempo que tarda en triangular
    start = time.time()
    T.triangulate(puntos, aristas)
    end = time.time()
    elapsed_time_ms = (end - start) * 1000

    print(f"Triangulacion hecha en: {elapsed_time_ms:.2f} ms")

    vertices, indices, restricted_edge_list, restricted_edge_colors, min_x, min_y, max_x, max_y = read_triangulation(T)

    range_x = abs(max_x - min_x)
    range_y = abs(max_y - min_y)
    zoom = max([range_x, range_y]) / 2

    controller.zoom = 0.8 / zoom
    controller.x = 0
    controller.y = 0

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

    # Crear el buffer para las aristas restringidas
    edge_vertices = []
    for edge in restricted_edge_list:
        v1_index = edge[0]
        v2_index = edge[1]
        edge_vertices.append(vertices[v1_index * 3:v1_index * 3 + 3])
        edge_vertices.append(vertices[v2_index * 3:v2_index * 3 + 3])
    edge_vertices_np = np.array(edge_vertices, dtype=np.float32).flatten()

    # Crear el buffer para los colores de las aristas restringidas
    edge_color = np.array([1.0, 0.0, 0.0], dtype=np.float32)  # Rojo para las aristas restringidas
    restricted_edge_colors = np.tile(edge_color, (len(restricted_edge_list) * 2, 1)).flatten()

    gpu_edges = pipeline.vertex_list(
        len(restricted_edge_list)*2, GL.GL_LINES,
    )
    gpu_edges.position[:] = edge_vertices_np
    gpu_edges.color[:] = restricted_edge_colors

    pipeline.use()

    @win.event
    def on_key_press(key, mod):
        global current_triangle_index
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
        elif key == pyglet.window.key.K:
            # Mover al triangulo anterior en la lista y actualizar LEPP
            if current_triangle_index > 0:
                current_triangle_index -= 1
                update_lepp_visualization()
        elif key == pyglet.window.key.L:
            # Mover al siguiente triangulo en la lista y actualizar LEPP
            if current_triangle_index < len(T.triangles) - 1:
                current_triangle_index += 1
                update_lepp_visualization()

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

        # Dibujar las aristas restringidas
        gpu_edges.draw(GL.GL_LINES)
        if gpu_green_edges:
            gpu_green_edges.draw(GL.GL_LINES)

    green_edges = []
    gpu_green_edges = None






    def update(time):
        controller.x += controller.vx
        controller.y += controller.vy

    pyglet.clock.schedule_interval(update, 1 / 60)

    pyglet.app.run()
