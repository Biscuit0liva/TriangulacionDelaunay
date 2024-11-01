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

    def __sub__(self, other):
        return point(self.x - other.x, self.y - other.y)
    
    def norm(self):
        return (self.x**2 + self.y**2)**0.5
    