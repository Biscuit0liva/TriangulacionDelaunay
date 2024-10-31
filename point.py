# Clase de puntos, representan los vertices
# Se construyen con sus coordenadas en x e y
class point:
    def __init__(self,x:float,y:float):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"Punto({self.x},{self.y})"
    
    def __eq__(self, other):
        if isinstance(other, point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    