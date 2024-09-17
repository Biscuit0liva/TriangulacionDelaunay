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
    
    # Metodo para remplazar el vecino por otro
    # recibe el triangulo t_old que sera remplzado como vecino por t_new
    def replace(self, t_old:'Triangle', t_new:'Triangle')->None:
        i_old = self.vecinos.index(t_old)       # posicion en la lista que remplzar
        self.vecinos[i_old] = t_new             # cambio el objeto en la posicion
