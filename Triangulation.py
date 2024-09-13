from point import point
from Triangle import Triangle
from utils import incircle, orient2d
# implementacion de la clase que representa la triangulacion
# Se compone de una lista con sus triangulos y otra con los puntos de su geometria contenedora

class Triangulation:
    def __init__(self):
        self.triangles = []     # lista de triangulos
        self.container = None     # geometria contenedora
    
    
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
        # asigno a los vecinos los triangulos nuevos
        

        # elimino los triangulos anteriores de la triangulacion
        self.delete(t1)
        self.delete(t2)