import unittest
import sys
import os

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from point import point
from Triangle import Triangle
from Edge import Edge

class TestEdge(unittest.TestCase):
    def test_intersect_with(self):
        e1 = Edge(point(-5.43,2.9), point(-4,-3))
        e2 = Edge(point(-6.25,-1.34), point(-2.79,1.3))
        self.assertTrue(e1.intersect_with(e2))
        self.assertTrue(e2.intersect_with(e1))
        e3 = Edge(point(-5.43,2.9), point(-1,3))
        # aristas que compartan un punto no se intersectan
        self.assertFalse(e1.intersect_with(e3))
        self.assertFalse(e3.intersect_with(e1))
        # prueba de que aristas que no se intersectan no dan positivo
        self.assertFalse(e3.intersect_with(e2))
        self.assertFalse(e2.intersect_with(e3))
        e4 = Edge(point(-7.41,3.88), point(-7.25,1.9))
        self.assertFalse(e4.intersect_with(e3))
        self.assertFalse(e3.intersect_with(e4))
        # prueba de aristas tangentes
        e5 = Edge(point(-1,2), point(-1,5))
        self.assertFalse(e5.intersect_with(e3))
        self.assertFalse(e3.intersect_with(e5))
        


if __name__ == '__main__':
    unittest.main()