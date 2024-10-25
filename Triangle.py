from point import point
from Edge import Edge
from utils import orient2d

# Clase que representa los triangulos
# se inicializa con 3 objetos de la clase point
# como convecion, seran construidos en sentido antihorario
# ademas, para representar aristas de estes seran referenciadas con su vertice opuesto
# como elementos, cada triangulo mantiene una lista de sus triangulos vecinos



class Triangle:
    def __init__(self,v1:int ,v2:int, v3:int):
        self.vertices = [v1, v2, v3]        # lista de vertices
        self.vecinos = [None, None, None]   # lista de triangulos vecinos
    
    def __eq__(self, other: 'Triangle') -> bool:
        if not isinstance(other, Triangle):
            return False
        return self.vertices == other.vertices or \
               self.vertices == [other.vertices[1], other.vertices[2], other.vertices[0]] or \
               self.vertices == [other.vertices[2], other.vertices[0], other.vertices[1]]
    
    def __repr__(self):
        return f"Triangulo[{self.vertices[0]}, {self.vertices[1]}, {self.vertices[2]}]"
    
    # getter de la arista opuesta al punto i
    # recibe el indice i del punto y retorna la tupla ordenada de puntos que la componen 
    def get_arista_opuesta(self, index: int) -> tuple[int,int]:
        return (self.vertices[(index+1)%3], self.vertices[(index+2)%3])
    
    # Asigna al triangulo un vecino
    # para ello lo hace respecto al vertice opuesto de la arista que comparten
    # Recibe el indice del vertice opuesto y el triangulo que incluira
    def set_vecino(self, index: int, vecino: 'Triangle')->None:
        self.vecinos[index] = vecino
    
    # Getter del vecino opuesto al i-esimo vertice
    # recibe el indice i del vertice opuesto
    def get_vecino_opuesto(self, index: int) -> 'Triangle':
        return self.vecinos[index]
    
    # Metodo para remplazar el vecino por otro
    # recibe el triangulo t_old que sera remplzado como vecino por t_new
    def replace(self, t_old:'Triangle', t_new:'Triangle')->None:
        i_old = self.vecinos.index(t_old)       # posicion en la lista que remplzar
        self.vecinos[i_old] = t_new             # cambio el objeto en la posicion

    # Metodo para verificar si una arista intersecta alguno de los lados del triangulo
    # recibe una arista, la lista de puntos de la triangulacion y retorna un booleano
    def is_intersected(self, edge:Edge, points: list[point]) -> bool:
        # extraemos los puntos del triangulo y la arista
        p1,p2,p3 = points[self.vertices[0]], points[self.vertices[1]], points[self.vertices[2]]
        e1, e2 = edge.p1, edge.p2
        print(f"p1: {p1}, p2: {p2}, e1: {e1}, e2: {e2}")
        # verificamos la interseccion con cada lado del triangulo usando orient2D
        if self.segments_intersect(p1,p2, e1, e2):
            return True
        if self.segments_intersect(p2,p3, e1, e2):
            return True
        if self.segments_intersect(p3,p1, e1, e2):
            return True
        return False
    
    # Metodo auxiliar para verificar si dos segmentos se intersectan, usando orient2D
    # recibe los puntos de los segmentos y retorna un booleano
    @staticmethod
    def segments_intersect(p1:point,p2:point, q1:point, q2:point):
        o1 = orient2d(p1, p2, q1,1e-10)
        o2 = orient2d(p1, p2, q2,1e-10)
        o3 = orient2d(q1, q2, p1,1e-10)
        o4 = orient2d(q1, q2, p2,1e-10)
        print(f"o1: {o1}, o2: {o2}, o3: {o3}, o4: {o4}")
        # si las orientaciones son diferentes, significa que estan en lados opuestos
        return o1*o2 < 0 and o3*o4 < 0
        
