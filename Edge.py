# Clase que representa aristas
# Se construye con dos puntos
from point import point
class Edge:
    def __init__(self, p1:int, p2:int):
        self.p1 = p1  # punto 1
        self.p2 = p2  # punto 2
        # Opcionalmente: podrías agregar vecinos u otros atributos necesarios más adelante.
    
    def __eq__(self, other):
        # Compara dos aristas, independientemente del orden de los puntos
        return {self.p1, self.p2} == {other.p1, other.p2}
    
    def __hash__(self):
        # Hace la arista "hashable", útil si quieres meterlas en un set
        return hash(frozenset([self.p1, self.p2]))
