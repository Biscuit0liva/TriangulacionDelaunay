# Clase de puntos, representan los vertices
# Se construyen con sus coordenadas en x e y
class point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"Punto({self.x},{self.y})"
    
    def __eq__(self, otro) -> bool:
        return self.x == otro.x and self.y == otro.y
    