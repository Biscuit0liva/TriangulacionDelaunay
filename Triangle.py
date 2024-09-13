from point import point

# Clase que representa los triangulos
# se inicializa con 3 objetos de la clase point
# como convecion, seran construidos en sentido antihorario
# ademas, para representar aristas de estes seran referenciadas con su vertice opuesto
# como elementos, cada triangulo mantiene una lista de sus triangulos vecinos



class Triangle:
    def __init__(self,v1 ,v2, v3):
        self.vertices = [v1, v2, v3]        # lista de vertices
        self.vecinos = [None, None, None]   # lista de triangulos vecinos

    # getter de la arista opuesta al punto i
    # recibe el indice i del punto y retorna la tupla ordenada de puntos que la componen 
    def get_arista_opuesta(self, index: int) -> tuple[point,point]:
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