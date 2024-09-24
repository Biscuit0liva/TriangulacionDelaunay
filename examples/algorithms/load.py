from Triangulation import Triangulation

def read_triangulation(T: Triangulation):
    vertex_list = []
    triangle_list = []
    min_x = float("inf")
    max_x = -float("inf")
    min_y = float("inf")
    max_y = -float("inf")
    for p in T.points[3:]:    # Evita los primeros 3 puntos que son los del contenedor
        x = p.x
        min_x = x if x < min_x else min_x
        max_x = x if x > max_x else max_x
        y = p.y
        min_y = y if y < min_y else min_x
        max_y = y if y > max_y else min_y
        z = 0.0
        vertex_list += [x, y, z]
    for t in T.triangles:
        triangle_list += [
            t.vertices[0]-3,
            t.vertices[1]-3,
            t.vertices[2]-3,
        ]
    return vertex_list, triangle_list, min_x, min_y, max_x, max_y