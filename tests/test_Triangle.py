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

    def test_replace(self):
        a = point(0, 0)
        b = point(1, 0)
        c = point(0, 1)
        d = point(2, 0)
        e = point(2,1)
        f = point(-1,1)
        g = point(0, -2)
        h = point(3,-2)
        # triangulos de prueba
        t1 = Triangle(a, b, c)
        t2 = Triangle(c,b,d)
        t3 = Triangle(d,e,c)
        t4 = Triangle(f,a,c)
        t5 = Triangle(b,a,g)
        t6 = Triangle(h,d,b)
        # seteamos sus vecinos
        t1.set_vecino(0,t2)
        t1.set_vecino(1, t4)
        t1.set_vecino(2, t5)
        # realizamos un remplazo de prueba, no necesariamente esta bien
        t1.replace(t4, t6)
        self.assertEqual(t1.vecinos[1], t6)

if __name__ == '__main__':
    unittest.main()
