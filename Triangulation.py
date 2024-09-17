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
        # creo los nuevos triangulos
        t1_new = Triangle(vi, vj, vl)
        t2_new = Triangle(vl, vk, vi)
        # asigno los vecinos a estos nuevos triangulos
        t1_new.set_vecino(0, t2.get_vecino_opuesto((i_2+1)%3))
        t1_new.set_vecino(1, t2_new)
        t1_new.set_vecino(2, t1.get_vecino_opuesto((i_1+2)%3))
        t2_new.set_vecino(0, t1.get_vecino_opuesto((i_1+1)%3))
        t2_new.set_vecino(1, t1_new)
        t2_new.set_vecino(2, t2.get_vecino_opuesto((i_2+2)%3))
        # remplazo en los vecinos los triangulos anteriores por los nuevos
        t1j = t1.get_vecino_opuesto((i_1+1)%3)
        t1k = t1.get_vecino_opuesto((i_1+2)%3)
        t2k = t2.get_vecino_opuesto((i_2+1)%3)
        t2j = t2.get_vecino_opuesto((i_2+2)%3)
        t1j.replace(t1, t2_new)
        t1k.replace(t1, t1_new)
        t2k.replace(t2, t1_new)
        t2j.replace(t2, t2_new)
        # elimino los triangulos anteriores de la triangulacion

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

        