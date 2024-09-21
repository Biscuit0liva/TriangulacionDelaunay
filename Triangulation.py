from point import point
from Triangle import Triangle
from utils import incircle, orient2d
# implementacion de la clase que representa la triangulacion
# Se compone de una lista con sus triangulos y otra con los puntos de su geometria contenedora

class Triangulation:
    def __init__(self, epsilon):
        self.triangles = []     # lista de triangulos
        self.container = None   # geometria contenedora
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
                if orient2d(point, v1, v2, self.epsilon) < 0:
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
        v0, v1, v2 = t.vertices
        t.vertices = [v0,v1,p]
        t2 = Triangle(v1,v2,p)
        t3 = Triangle(v2,v0,p)
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
        ta.vertices = [vi, vj, p]
        t4 = Triangle(vk, vi, p)
        tb.vertices = [vl, vk, p]
        t2 = Triangle(vj, vl,p)
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

    def legalize_edge(self, t1: Triangle, t2:Triangle):
        # vertice opuesto a la arista compartida en t2
        p = t1.vertices[(t1.vecinos.index(t2))]
        # verificar la condicion de delaunay en t1
        if incircle(p, t2.vertices[0], t2.vertices[1], t2.vertices[2], self.epsilon)>=0:  # tomamos en el circulo como adentro
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

    
        