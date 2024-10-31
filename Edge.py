# Clase que representa aristas
# Se construye con dos puntos
from point import point
from utils import orient2d
class Edge:
    def __init__(self, p1:int, p2:int):
        self.p1 = p1  # punto 1
        self.p2 = p2  # punto 2
        # Opcionalmente: podrías agregar vecinos u otros atributos necesarios más adelante.
    
    def __eq__(self, other):
        # Compara dos aristas, independientemente del orden de los puntos
        return {self.p1, self.p2} == {other.p1, other.p2}
    
    def __repr__(self):
        # Representación de la arista
        return f"Arista({self.p1},{self.p2})"
    
    def __hash__(self):
        # Hace la arista "hashable", útil si quieres meterlas en un set
        return hash(frozenset([self.p1, self.p2]))
    
    # Verifica si se intersecta con otra arista, retornando un booleano
    def intersect_with(self, other: 'Edge') -> bool:
        # Usamos orient2D para verificar la intersección
        o1 = orient2d(other.p1, self.p1, self.p2, 1e-10)
        o2 = orient2d(other.p2, self.p1, self.p2, 1e-10)
        o3 = orient2d(self.p1, other.p1, other.p2, 1e-10)
        o4 = orient2d(self.p2, other.p1, other.p2, 1e-10)
        # la interseccion ocurre si los puntos estan en lados opuestos de la arista en cada segmento
        return o1*o2 < 0 and o3*o4 < 0





