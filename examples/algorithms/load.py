from Triangulation import Triangulation

def read_triangulation(T: Triangulation):
    vertex_list = []
    triangle_list = []
    restricted_edge_list = []   # Solo las aristas restringidas
    restricted_edge_colors = [] 
    min_x = float("inf")
    max_x = -float("inf")
    min_y = float("inf")
    max_y = -float("inf")
    for p in T.points:
        x = p.x
        min_x = x if x < min_x else min_x
        max_x = x if x > max_x else max_x
        y = p.y
        min_y = y if y < min_y else min_y
        max_y = y if y > max_y else max_y
        z = 0.0
        vertex_list += [x, y, z]
    for t in T.triangles:   # corrijo el desplazamiento de indices
        triangle_list += [
            t.vertices[0],
            t.vertices[1],
            t.vertices[2],
        ]
    if T.edges is not None:
        for edge in T.edges:
            restricted_edge_list += [(T.points.index(edge.p1), T.points.index(edge.p2))]
            restricted_edge_colors.extend([1.0,0.0,0.0]*2)  # Color rojo
    return vertex_list, triangle_list, restricted_edge_list, restricted_edge_colors, min_x, min_y, max_x, max_y