import random
from point import point
from Triangle import Triangle
from Edge import Edge
from utils import incircle, orient2d
# implementacion de la clase que representa la triangulacion
# Se compone de una lista con sus los puntos,un contador de los puntos, una lista con sus triangulos, 
# , su geometria contenedora y la tolerancia epsilon que usa en los predicados

class Triangulation:
    def __init__(self, minx, maxx, miny, maxy, epsilon):
        self.points = []        # lista de puntos
        self.cnt = 0            # contador de puntos
        self.triangles = []     # lista de triangulos
        self.edges = []         # lista de aristas restringidas
        self.minx = minx        # cordenada de los puntos mas pequeña en el eje x
        self.maxx = maxx        # cordenada de los puntos mas grande en el eje x
        self.miny = miny        # cordenada de los puntos mas pequeña en el eje y
        self.maxy = maxy        # cordenada de los puntos mas grande en el eje y
        self.epsilon = epsilon  # tolerancia de la triangulacion
    
    
    # Realiza un flip en la arista compartida entre los triángulos t1 y t2.
    # realiza los cambios sobre la misma referencia de los triangulos, evitando
    # Recibe los triangulos t1 y t2 que son adyacentes
    def flip(self, t1:Triangle, t2:Triangle):
        # busco el indice correspondiente a cada vecino
        i_1 = t1.vecinos.index(t2)                       # punto de t1 al que es opuesto t2
        i_2 = t2.vecinos.index(t1)                       # punto de t2 al que es opuesto t1
        arista_compartida = t1.get_arista_opuesta(i_1)   # vj vk
        # obtengo los vertices
        vi = t1.vertices[i_1]
        vj,vk = arista_compartida
        vl = t2.vertices[i_2]
        # extraigo los vecinos de los triangulo ta y tb
        t1j = t1.get_vecino_opuesto((i_1+1)%3)
        t1k = t1.get_vecino_opuesto((i_1+2)%3)
        t2k = t2.get_vecino_opuesto((i_2+1)%3)
        t2j = t2.get_vecino_opuesto((i_2+2)%3)
        # modifico t1 y t2
        t1.vertices = [vi, vj, vl]
        t2.vertices = [vl, vk, vi]
        # reasigno los vecinos a estos nuevos triangulos
        t1.set_vecino(0, t2k)
        t1.set_vecino(1, t2)
        t1.set_vecino(2, t1k)
        t2.set_vecino(0, t1j)
        t2.set_vecino(1, t1)
        t2.set_vecino(2, t2j)
        # actualizar los vecinos anteriores de t1 y t2 (si existen)
        if t1j is not None:
            t1j.replace(t1, t2)
        if t1k is not None:
            t1k.replace(t1, t1)
        if t2k is not None:
            t2k.replace(t2, t1)
        if t2j is not None:
            t2j.replace(t2, t2)

    # Busca el triangulo que contenga el punto recibido, recorriendo los triangulos
    # Recorre usando orient2D en las aristas con el punto y avanza cuando el punto este a la derecha
    # se detiene cuando todas las aristas tengan el punto a su izquierda
    # En el caso de que el punto este en una arista, retorna el primer triangulo que tiene esa arista
    def find_containing_triangle(self, point:point) -> Triangle:
        # Comienzo por el primer triangulo, que sera uno contenedor posiblemente
        current_triangle = self.triangles[0]

        while True:
            inside = True  # Asume que está dentro hasta que se pruebe lo contrario

            for i in range(3):
                # Obtener los dos puntos de la arista opuesta al vértice i
                v1, v2 = current_triangle.get_arista_opuesta(i)
                
                # Si orient2D devuelve negativo, el punto está fuera del lado de la arista
                if orient2d(point, self.points[v1], self.points[v2], self.epsilon) < 0:
                    inside = False
                    # Moverse al triángulo que comparte la arista
                    current_triangle = current_triangle.vecinos[i]
                    break  # Sale del ciclo para evaluar el siguiente triángulo

            if inside:
                return current_triangle  # Se encontró el triángulo que contiene el punto
            
    # metodo para insertar un punto en un triangulo
    # Esto generara 3 triangulos nuevos, el metodo maneja la actualizacion de vecinos
    # recibe el indice del triangulo en la triangulacion y el punto que se inserta
    def insert3(self, t:Triangle, p:point):
        self.points.append(p)
        self.cnt += 1               # incrementar el contador de puntos
        x = self.cnt - 1            # indice del punto insertado
        v0, v1, v2 = t.vertices
        t.vertices = [v0,v1,x]
        t2 = Triangle(v1,v2,x)
        t3 = Triangle(v2,v0,x)
        # vecinos anteriores de t
        # actualizar los vecinos de t (si existen) antes setear sus nuevos vecinos t2 y t3
        vecino0 = t.get_vecino_opuesto(0)
        vecino1 = t.get_vecino_opuesto(1)
        vecino2 = t.get_vecino_opuesto(2)
        # actualizar referencia de vecinos
        t.set_vecino(0,t2)
        t.set_vecino(1,t3)
        t.set_vecino(2,vecino2)
        t2.set_vecino(0,t3)
        t2.set_vecino(1,t)
        t2.set_vecino(2,vecino0)
        t3.set_vecino(0,t)
        t3.set_vecino(1,t2)
        t3.set_vecino(2,vecino1)
        # actualizar los vecinos de t (si existen)
        if vecino0 is not None:
            vecino0.replace(t,t2)
        if vecino1 is not None:
            vecino1.replace(t,t3)
        #if vecino2 is not None:
        #    vecino2.replace(t,t1)
        # agregar t2 y t3 a la lista
        self.triangles.append(t2)
        self.triangles.append(t3)

    # metodo para insertar un punto en un triangulo
    # esto genera 4 triangulos nuevos
    # se utilza para el caso que un punto se inserte en una arista
    # Recibe los dos triangulos que comparten la arista y el punto a insertar
    def insert4(self, ta: Triangle, tb: Triangle, p:point):
        self.points.append(p)
        self.cnt += 1               # incrementar el contador de puntos
        x = self.cnt - 1            # indice del punto insertado
        # busco el indice correspondiente a cada vecino
        i_a = ta.vecinos.index(tb)                       # punto de ta al que es opuesto tb
        i_b = tb.vecinos.index(ta)                       # punto de tb  al que es opuesto ta
        # vertices
        vi = ta.vertices[i_a]                   # vertice opuesto a tb
        vj, vk = ta.get_arista_opuesta(i_a)     # ta = vi, vj, vk tb = vl, vk, vj (no necesariamente en ese orden)
        vl = tb.vertices[i_b]                   # vertice opuesto a ta
        # extraigo los vecinos de los triangulo ta y tb
        taj = ta.get_vecino_opuesto((i_a+1)%3)
        tak = ta.get_vecino_opuesto((i_a+2)%3)
        tbk = tb.get_vecino_opuesto((i_b+1)%3)
        tbj = tb.get_vecino_opuesto((i_b+2)%3)
        # modifico ta y tb, se crea t2 y t4 los otros dos que se generan
        # los triangulos quedarian en orden anti horario: ta, t2, tb, t4
        ta.vertices = [vi, vj, x]
        t4 = Triangle(vk, vi, x)
        tb.vertices = [vl, vk, x]
        t2 = Triangle(vj, vl,x)
        # seteamos los vecinos
        ta.set_vecino(0,t2)
        ta.set_vecino(1,t4)
        ta.set_vecino(2,tak)
        t2.set_vecino(0,tb)
        t2.set_vecino(1,ta)
        t2.set_vecino(2,tbk)
        tb.set_vecino(0,t4)
        tb.set_vecino(1,t2)
        tb.set_vecino(2,tbj)
        t4.set_vecino(0,ta)
        t4.set_vecino(1,tb)
        t4.set_vecino(2,taj)
        # actualizar los vecinosa anteriores de ta y tb (si existen)
        #if tak is not None:
         #   tak.replace(ta,ta)
        if tbk is not None:
            tbk.replace(tb,t2)
        #if tbj is not None:
         #   tbj.replace(tb,tb)
        if taj is not None:
            taj.replace(ta,t4)
        # agregar t2 y t4 a la lista
        self.triangles.append(t2)
        self.triangles.append(t4)

    # Metodo para legalizar una arista
    # Recibe los dos triangulos que comparten la arista
    # Si la arista no cumple la condicion de delaunay, se realiza un flip
    # y se llama recursivamente para legalizar las nuevas aristas
    def legalize_edge(self, t1: Triangle, t2:Triangle):
        # vertice opuesto a la arista compartida en t2
        p = t1.vertices[(t1.vecinos.index(t2))]
        # verificar la condicion de delaunay en t1
        if incircle(self.points[p], self.points[t2.vertices[0]], self.points[t2.vertices[1]], self.points[t2.vertices[2]], self.epsilon)>=0:  # tomamos en el circulo como adentro
            # ilegal
            self.flip(t1, t2)
            # busco los indices de p en t1 y t2 despues del flip
            i_1 =t1.vertices.index(p)
            i_2 =t2.vertices.index(p)
            # legalizacion recursiva
            vecino_1 = t1.get_vecino_opuesto(i_1)
            vecino_2 = t2.get_vecino_opuesto(i_2)
            if vecino_1 is not None:
                self.legalize_edge(t1, vecino_1)  # Para la nueva arista E1
            if vecino_2 is not None:
                self.legalize_edge(t2, vecino_2)  # Para la nueva arista E2


    # Metodo que verifica si un punto esta en una arista del triangulo
    # retorna el booleano y el indice del vecino en su lista de vecinos que lo comparte
    def point_on_edge(self, p:point, t:Triangle):
        for i in range(3):
            v1, v2 = t.get_arista_opuesta(i)
            if orient2d(p, self.points[v1], self.points[v2], self.epsilon) == 0:
                return True, i
        return False, None

    # Metodo que encuentra el primer triangulo de la triangulacion que intersecta una arista
    # recibe una arista y retorna el primer triangulo que intersecta
    def find_first_intersect(self, edge: Edge) -> Triangle:
        current_triangle = self.triangles[0]
        visited = set()  # para marcar los triangulos que ya se visitaron
        while True:
            if current_triangle in visited:
                return None
            visited.add(current_triangle)
            # verificar si el triangulo actual contiene al punto inicial de la arista
            if edge.p1 in [self.points[v] for v in current_triangle.vertices]:
                # verificar si la arista intersecta el triangulo
                for i in range(3):
                    v1, v2 = current_triangle.get_arista_opuesta(i)
                    arista_compartida = Edge(self.points[v1], self.points[v2])
                    if arista_compartida.intersect_with(edge):
                        # si intersecta, el triangulo actual es el primero que intersecta la arista
                        return current_triangle
                # si no intersecta, avanzar en direccion al punto p1 de la arista
                for i in range(3):
                    # obtener los dos puntos de la arista opuesta al vértice i
                    v1, v2 = current_triangle.get_arista_opuesta(i)
                    o = orient2d(edge.p1, self.points[v1], self.points[v2], self.epsilon)
                    # si orient2D devuelve negativo, el punto está fuera del lado de la arista
                    if  o<= 0 and current_triangle.vecinos[i] is not None:
                        # revisar que no es uno ya visitdo
                        if current_triangle.vecinos[i] not in visited:
                            current_triangle = current_triangle.vecinos[i]
                            break
            else:
                # Si no lo contiene, solo avanzo en direccion al punto p1 de la arista
                for i in range(3):
                    # obtener los dos puntos de la arista opuesta al vértice i
                    v1, v2 = current_triangle.get_arista_opuesta(i)
                    # si orient2D devuelve negativo, el punto está fuera del lado de la arista
                    if orient2d(edge.p1, self.points[v1], self.points[v2], self.epsilon) < 0:
                        # moverse al triángulo que comparte la arista
                        current_triangle = current_triangle.vecinos[i]
                        break

                    
    # encuentra todos los triangulos de la triangulacion (en orden) que intersectan una arista dada
    # recibe una arista y retorna una lista de triangulos
    def find_triangles_intersecting_edge(self, edge: Edge) -> list[Triangle]:
        # primero, encuentra el primer triangulo que tiene el punto p_i e intersecta la arista
        start_triangle = self.find_first_intersect(edge)
        if start_triangle is None:
            return []   # si no encuentra un triangulo, retorna una lista vacia
        
        visited = set()  # para marcar los triangulos que ya se visitaron
        intersected_triangles = []  # lista de triangulos que intersectan la arista
        current_triangle = start_triangle  # comienza en el primer triangulo
        previous_triangle = None
        while current_triangle and current_triangle not in visited:
            visited.add(current_triangle)   # Marcar como visitado
            intersected_triangles.append(current_triangle)  # Agregar a la lista de triangulos intersectados
            
            # Encuentra el vecino cuya arista compartida intersecta la arista restringida
            for i,vecino in enumerate(current_triangle.vecinos):
                if vecino and vecino != previous_triangle:
                    v1, v2 = current_triangle.get_arista_opuesta(i)
                    arista_compartida = Edge(self.points[v1], self.points[v2])
                    if arista_compartida.intersect_with(edge):
                        previous_triangle = current_triangle
                        current_triangle = vecino
                        break
            else:
                #print(f"No se encontro vecino, se sale del loop, ultimo triangulo: {current_triangle}")
                break
        return intersected_triangles

    # Encuentra los segmentos colineales a una arista
    # Recibe una lista de triangulos en orden, para buscar puntos colineales
    # Retorna una lista de listas de triangulos, correspondientes a los segmentos colineales
    def find_collinear_segments(self, triangles: list[Triangle], edge:Edge):
        collinear_segments = [edge.p1, edge.p2]  # lista de segmentos colineales

        for triangle in triangles:
            for vertex in triangle.vertices:
                point = self.points[vertex]
                # Evita agregar los puntos de la arista
                if point != edge.p1 or point != edge.p2:
                    continue
                # Si el punto es colineal con la arista, agregarlo a la lista
                if orient2d(edge.p1, edge.p2, point, self.epsilon) == 0:
                    collinear_segments.append(point)

        return collinear_segments
    
    # Recibe una arista y la inserta en la triangulacion
    def insert_edge(self, edge:Edge):
        # Encontrar camino de triangulos intersectados por la arista
        intersected_triangles = self.find_triangles_intersecting_edge(edge)
        # conjunto de cuadrilateros ya flipados
        flipped_quads = set()
        # Itero mientras la arista no sea aun construida
        while len(intersected_triangles)>0:
            # Itero sobre pares de triangulos consecutivos en el camino
            for i in range(len(intersected_triangles)-1):
                t1 = intersected_triangles[i]
                t2 = intersected_triangles[i+1]
                if self.can_flip(t1,t2):
                    # Obtener los vértices del cuadrilátero
                    i_1 = t1.vecinos.index(t2)
                    i_2 = t2.vecinos.index(t1)
                    vi = t1.vertices[i_1]
                    vj, vk = t1.get_arista_opuesta(i_1)
                    vl = t2.vertices[i_2]
                    quadrilateral = tuple(sorted([vi, vj, vk, vl]))
                    # Verificar si el cuadrilátero ya fue flipado
                    if quadrilateral not in flipped_quads:
                        self.flip(t1, t2)
                        flipped_quads.add(quadrilateral)
                        # actualizar el path de triangulos intersectados
                        intersected_triangles = self.find_triangles_intersecting_edge(edge)
                        break


    # Metodo que verifica si se puede realizar un flip en una arista
    # Entre dos triangulos, determina si forman un poligono convexo
    # Recibe dos triangulos adyacentes y retorna un booleano
    def can_flip(self, t1:Triangle, t2:Triangle):
        # Busco la arista compartida
        i_1 = t1.vecinos.index(t2)                       # punto de t1 al que es opuesto t2
        i_2 = t2.vecinos.index(t1)                       # punto de t2 al que es opuesto t1
        arista_compartida = t1.get_arista_opuesta(i_1)   # vj vk
        # obtengo los vertices
        vi = t1.vertices[i_1]
        vj,vk = arista_compartida
        vl = t2.vertices[i_2]
        # extraigo los puntos
        vi = self.points[vi]
        vj = self.points[vj]
        vk = self.points[vk]
        vl = self.points[vl]
        # verificar convexidad usando orientaciones
        if (orient2d(vi,vj,vl, self.epsilon)>0 and
            orient2d(vj,vl,vk, self.epsilon)>0 and
            orient2d(vl,vk,vi, self.epsilon)>0 and
            orient2d(vk,vi,vj, self.epsilon)>0):
            return True
        else:
            return False
        




        

    # Metodo que realiza la triangulacion
    # Recibe una lista de puntos, aristas y realiza la triangulacion de Delaunay
    # Se inicializa la triangulacion con un triangulo contenedor
    # Se recorren los puntos y se insertan uno a uno
    # Al terminar, quedan los indices de los puntos de los triangulos desplazados por 3.
    # Esto se corrige recorriendo los triangulos y cambiando sus indices de puntos
    def triangulate(self, points, edges = None):
        # Crear un triángulo contenedor
        p1 = point(self.minx-1e6, self.miny-1e6)
        p2 = point(self.maxx+1e6, self.miny-1e6)
        p3 = point(0, self.maxy+1e6)
        # agregarlos a la lista de puntos
        self.points.append(p1)
        self.points.append(p2)
        self.points.append(p3)
        self.cnt += 3   # incrementar el contador de puntos
        # crear el triangulo contenedor
        container = Triangle(0, 1, 2)
        self.triangles.append(container)
        # preprocesamiento para las aristas restringidas. Por ahora asumo que no hay aristas que se intersecten
        # agregar los vertices de las aristas restringidas a la lista de puntos si es que no estan
        if edges is not None:
            for edge in edges:
                if edge.p1 not in points:
                    points.append(edge.p1)
                if edge.p2 not in points:
                    points.append(edge.p2)
            # Revisar que no hayan puntos en las aristas, si los hay, se segmenta la aristas con este punto
            for edge in edges:
                for p in points:
                    if p in [edge.p1, edge.p2]:
                        continue
                    # verifica colinealidad y si el punto esta dentro del segmento
                    if (orient2d(p, edge.p1, edge.p2, self.epsilon) == 0 and
                        min(edge.p1.x, edge.p2.x) <= p.x <= max(edge.p1.x, edge.p2.x) and
                        min(edge.p1.y, edge.p2.y) <= p.y <= max(edge.p1.y, edge.p2.y)):
                        # segmentar la arista
                        edge1 = Edge(edge.p1, p)
                        edge2 = Edge(p, edge.p2)
                        edges.append(edge1)
                        edges.append(edge2)
                        edges.remove(edge)
        self.edges = edges
        # permutacion aleatoria de los puntos
        points = random.sample(points, len(points))
        # recorrer los puntos y agregarlos a la triangulacion
        for p in points:
            # encontrar el triangulo que contiene el punto
            t = self.find_containing_triangle(p)
            # revisa si el punto esta en la arista
            on_edge, i_neighbour = self.point_on_edge(p,t)
            if on_edge:
                # insertar el punto en la arista
                tn = t.get_vecino_opuesto(i_neighbour)
                self.insert4(t, tn, p)
                # legalizar las aristas, para ello primero saco los 2 nuevos triangulos en la lista
                t2 = self.triangles[-2]
                t4 = self.triangles[-1]
                # legalizar las aristas (si existen)
                if t.get_vecino_opuesto(t.vertices.index(self.cnt-1)) is not None:
                    self.legalize_edge(t, t.get_vecino_opuesto(t.vertices.index(self.cnt-1)))   # esto es legalizar con el triangulo nuevo y su vecino opuesto al punto insertado
                if t2.get_vecino_opuesto(t2.vertices.index(self.cnt-1)) is not None:
                    self.legalize_edge(t2, t2.get_vecino_opuesto(t2.vertices.index(self.cnt-1)))
                if tn.get_vecino_opuesto(tn.vertices.index(self.cnt-1)) is not None:
                    self.legalize_edge(tn, tn.get_vecino_opuesto(tn.vertices.index(self.cnt-1)))
                if t4.get_vecino_opuesto(t4.vertices.index(self.cnt-1)) is not None:
                    self.legalize_edge(t4, t4.get_vecino_opuesto(t4.vertices.index(self.cnt-1)))
            else:
                # insertar el punto en el triangulo
                self.insert3(t, p)
                # legalizar las aristas, para ello primero saco los 2 nuevos triangulos en la lista
                t2 = self.triangles[-2]
                t3 = self.triangles[-1]
                # legalizar las aristas (si existen)
                if t.get_vecino_opuesto(t.vertices.index(self.cnt-1)) is not None:
                    self.legalize_edge(t, t.get_vecino_opuesto(t.vertices.index(self.cnt-1)))
                if t2.get_vecino_opuesto(t2.vertices.index(self.cnt-1)) is not None:
                    self.legalize_edge(t2, t2.get_vecino_opuesto(t2.vertices.index(self.cnt-1)))
                if t3.get_vecino_opuesto(t3.vertices.index(self.cnt-1)) is not None:
                    self.legalize_edge(t3, t3.get_vecino_opuesto(t3.vertices.index(self.cnt-1)))
        # recorrer las aristas restringidas y agregarlas a la triangulacion
        if edges is not None:
            for edge in edges:
                self.insert_edge(edge)


        # remover el triangulo contenedor
        triangles_to_remove = [t for t in self.triangles if any(v in [0, 1, 2] for v in t.vertices)]
        self.triangles = [t for t in self.triangles if t not in triangles_to_remove]
        
        # eliminar de los vecinos los triangulo con indice 0,1,2 y corregir indices al remover los 3 primeros puntos
        for t in self.triangles:
            for i in range(3):
                if t.vecinos[i] is not None and t.vecinos[i] in triangles_to_remove:
                    t.vecinos[i] = None
            
        for t in self.triangles:
            t.vertices = [v - 3 for v in t.vertices]
        self.points = self.points[3:]
        self.cnt -= 3


    # Metodo que entrega el lado mas largo de un triangulo
    # En caso de que algunos lados sean iguales, tomara el primero que encuentre
    # Siguiendo el orden en que se definen los vertices del triangulo
    # Recibe un triangulo y retorna el indice del vertice opuesto al lado mas largo
    def longest_edge(self, t:Triangle):
        e0a, e0b = t.get_arista_opuesta(0)
        e1a, e1b = t.get_arista_opuesta(1)
        e2a, e2b = t.get_arista_opuesta(2)

        l0 = (self.points[e0a]-self.points[e0b]).norm()
        l1 = (self.points[e1a]-self.points[e1b]).norm()
        l2 = (self.points[e2a]-self.points[e2b]).norm()
        if l0 >= l1 and l0 >= l2:
            return 0
        elif l1 >= l0 and l1 >= l2:
            return 1
        else:
            return 2
        

    # Metodo que encuentra LEPP en la triangulacion
    # Recibe un triangulo y retorna el LEPP de este como una lista
    def find_lepp(self, t:Triangle):
        lepp = [t]
        current_triangle = t
        while True:
            longest_edge = self.longest_edge(current_triangle)
            vecino = current_triangle.vecinos[longest_edge]
            # Primera condicione de termino, si se llega al borde de la triangulacion
            # Segunda condicion de termino, si es una arista terminal (la arista mas larga es la que comparte con el triangulo anterior en LEPP)
            if vecino is None or (len(lepp)>1 and vecino == lepp[-2]):
                break
            # Si no se termino, se agrega el vecino y se sigue buscando
            lepp.append(vecino)
            current_triangle = vecino
        return lepp

    
        