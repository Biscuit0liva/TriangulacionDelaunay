import unittest
import sys
import os

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from point import point
from Triangle import Triangle

class TestTriangle(unittest.TestCase):
    def test_creacion_triangulo(self):
        p1 = point(0, 0)
        p2 = point(1, 0)
        p3 = point(0, 1)
        tri = Triangle(p1, p2, p3)
        
        # Verifica que los vértices estén correctamente asignados
        self.assertEqual(tri.vertices[0], p1)
        self.assertEqual(tri.vertices[1], p2)
        self.assertEqual(tri.vertices[2], p3)
    
    def test_get_arista_opuesta(self):
        p1 = point(0, 0)
        p2 = point(1, 0)
        p3 = point(0, 1)
        tri = Triangle(p1, p2, p3)
        
        # Verificar que get_arista devuelve los puntos correctos
        arista = tri.get_arista_opuesta(0)
        self.assertEqual(arista, (p2, p3))  # La arista opuesta a p1

if __name__ == '__main__':
    unittest.main()
