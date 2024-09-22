
class Triangulation:
    """
    Clase que representa una triangulación de Delaunay.
    Considere implementar distintas clases en src para representar los triángulos y los puntos de la triangulación.
    """

    def __init__(self):
        """
        Defina una estructura adecuada para almacenar los triángulos y los puntos de la triangulación.
        Se recomienda usar una estructura basada en la cara de los triángulos con referencias a los triángulos vecinos.
        """
        self.triangles = []
        self.points = []
        self.container = None

    """
    Implemente los métodos necesarios para construir la triangulación de Delaunay.
    """
