import unittest
import sys
import os

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from point import point
from Triangle import Triangle
from Triangulation import Triangulation

class TestTriangle(unittest.TestCase):
    def setUp(self):
        self.T = Triangulation(1e-10)
        # puntos
        self.a = point(0, 0)
        self.b = point(1, -1)
        self.c = point(1, 1)
        self.d = point(2, 0)
        self.e = point(2, 1)
        self.f = point(-1, 1)
        self.g = point(0, -2)
        self.h = point(3, -2)

        # triangulos de prueba
        self.t1 = Triangle(self.a, self.b, self.c)
        self.t2 = Triangle(self.c, self.b, self.d)
        self.t3 = Triangle(self.d, self.e, self.c)
        self.t4 = Triangle(self.f, self.a, self.c)
        self.t5 = Triangle(self.b, self.a, self.g)
        self.t6 = Triangle(self.h, self.d, self.b)

        # seteamos sus vecinos
        self.t1.set_vecino(0, self.t2)
        self.t1.set_vecino(1, self.t4)
        self.t1.set_vecino(2, self.t5)
        self.t2.set_vecino(0, self.t6)
        self.t2.set_vecino(1, self.t3)
        self.t2.set_vecino(2, self.t1)
        self.t3.set_vecino(1, self.t2)
        self.t4.set_vecino(0, self.t1)
        self.t5.set_vecino(2, self.t1)
        self.t6.set_vecino(0, self.t2)

        # agregamos los triangulos a la triangulación
        self.T.triangles.append(self.t1)
        self.T.triangles.append(self.t6)
        self.T.triangles.append(self.t5)
        self.T.triangles.append(self.t4)
        self.T.triangles.append(self.t3)
        self.T.triangles.append(self.t2)

    def tearDown(self):
        # Limpieza: aquí podrías resetear o borrar variables si fuera necesario
        self.T = None
    
    def test_flip(self):
        # realizamos el flip
        self.T.flip(self.t1, self.t2)
        # comprobamos que se realizo bien
        t1_new = self.t4.get_vecino_opuesto(0)
        t2_new = self.t6.get_vecino_opuesto(0)
        # puntos bien asignados
        self.assertEqual(t1_new, Triangle(self.a, self.d, self.c))
        self.assertEqual(t2_new, Triangle(self.b, self.d, self.a))
        # que tenga sus vecinos bien asignados
        self.assertIn(t2_new,t1_new.vecinos)
        self.assertIn(self.t4,t1_new.vecinos)
        self.assertIn(self.t3,t1_new.vecinos)
        self.assertIn(t1_new,t2_new.vecinos)
        self.assertIn(self.t5,t2_new.vecinos)
        self.assertIn(self.t6,t2_new.vecinos)
        # revisamos que los triangulos quedaron con los vecinos bien
        self.assertEqual(t2_new, self.t5.get_vecino_opuesto(2))
        self.assertEqual(t1_new, self.t3.get_vecino_opuesto(1))
    
    def test_find_containing_triangle(self):
        # buscamos un punto en t1
        p1 = point(0.3,-0.1)
        self.assertEqual(self.T.find_containing_triangle(p1), self.t1)
        # buscamos un punto en t2
        p2 = point(1.35381,0.13697)
        self.assertEqual(self.T.find_containing_triangle(p2), self.t2)
        # buscamos un punto en t3
        p3 = point(1.14366,0.92076)
        self.assertEqual(self.T.find_containing_triangle(p3), self.t3)
        # buscamos un punto en t4
        p4 = point(-0.90669,0.94348)
        self.assertEqual(self.T.find_containing_triangle(p4), self.t4)
        # buscamos un punto en t5
        p5 = point(0.04181,-0.18109)
        self.assertEqual(self.T.find_containing_triangle(p5), self.t5)
        # buscamos un punto en t6
        p6 = point(2.41022,-1.47037)
        self.assertEqual(self.T.find_containing_triangle(p6), self.t6)
    


if __name__ == '__main__':
    unittest.main()
