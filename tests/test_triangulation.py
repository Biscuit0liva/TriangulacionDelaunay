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
        self.a = point(0, 0)    # 0
        self.b = point(1, -1)   # 1  
        self.c = point(1, 1)    # 2
        self.d = point(2, 0)    # 3
        self.e = point(2, 1)    # 4
        self.f = point(-1, 1)   # 5
        self.g = point(0, -2)   # 6
        self.h = point(3, -2)   # 7

        self.T.points = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        self.T.cnt = 8

        # triangulos de prueba
        self.t1 = Triangle(0, 1, 2)
        self.t2 = Triangle(2, 1, 3)
        self.t3 = Triangle(3, 4, 2)
        self.t4 = Triangle(5, 0, 2)
        self.t5 = Triangle(1, 0, 6)
        self.t6 = Triangle(7, 3, 1)

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
        t1_new = self.t6.get_vecino_opuesto(0)
        t2_new = self.t4.get_vecino_opuesto(0)
        # puntos bien asignados
        self.assertEqual(t1_new, Triangle(1, 3, 0))
        self.assertEqual(t2_new, Triangle(0, 3, 2))
        self.assertEqual(self.T.triangles[0], Triangle(1, 3, 0))
        self.assertEqual(self.T.triangles[5], Triangle(0, 3, 2))
        # que tenga sus vecinos bien asignados
        self.assertEqual(self.T.triangles[0],self.T.triangles[5].get_vecino_opuesto(1))
        self.assertEqual(self.T.triangles[3],self.T.triangles[5].get_vecino_opuesto(0))
        self.assertEqual(self.T.triangles[4],self.T.triangles[5].get_vecino_opuesto(2))
        self.assertEqual(self.T.triangles[5],self.T.triangles[0].get_vecino_opuesto(1))
        self.assertEqual(self.T.triangles[2],self.T.triangles[0].get_vecino_opuesto(2))
        self.assertEqual(self.T.triangles[1],self.T.triangles[0].get_vecino_opuesto(0))
        # revisamos que los triangulos quedaron con los vecinos bien
        self.assertEqual(self.T.triangles[0], self.T.triangles[2].get_vecino_opuesto(2))
        self.assertEqual(None, self.T.triangles[2].get_vecino_opuesto(0))
        self.assertEqual(None, self.T.triangles[2].get_vecino_opuesto(1))
        self.assertEqual(self.T.triangles[0], self.T.triangles[1].get_vecino_opuesto(0))
        self.assertEqual(None, self.T.triangles[1].get_vecino_opuesto(1))
        self.assertEqual(None, self.T.triangles[1].get_vecino_opuesto(2))
        self.assertEqual(self.T.triangles[5], self.T.triangles[4].get_vecino_opuesto(1))
        self.assertEqual(None, self.T.triangles[4].get_vecino_opuesto(0))
        self.assertEqual(None, self.T.triangles[4].get_vecino_opuesto(2))
        self.assertEqual(self.T.triangles[5], self.T.triangles[3].get_vecino_opuesto(0))
        self.assertEqual(None, self.T.triangles[3].get_vecino_opuesto(1))
        self.assertEqual(None, self.T.triangles[3].get_vecino_opuesto(2))
    
    def test_find_containing_triangle(self):
        # buscamos un punto en t1
        p1 = point(0.3,-0.1)
        self.assertEqual(self.T.find_containing_triangle(p1), self.t1)
        self.assertEqual(self.t1, self.T.triangles[0])
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
        # buscamos un punto en la arista compartida de t1 y t2
        p7 = point(1,-0.65)
        self.assertEqual(self.T.find_containing_triangle(p7), self.t1)
        # buscamos un punto en la arista compartida de t4
        p8 = point(-0.21,0.21)
        self.assertEqual(self.T.find_containing_triangle(p8), self.t4)
        # buscamos un punto en la arista de t6
        p9 = point(2.55,-1.11)
        self.assertEqual(self.T.find_containing_triangle(p9), self.t6)
    
    def test_insert3(self):
        # insertamos un punto en t1
        p1 = point(0.3,-0.1)
        self.T.insert3(self.T.triangles[0], p1)
        # vemos si se agrego el punto a la lista de puntos
        self.assertEqual(self.T.points[8], p1)
        self.assertEqual(self.T.cnt, 9)
        # comprobamos que modifico el objeto y no solo el de la lista
        self.assertEqual(self.t1, self.T.triangles[0])
        # comprobamos que se generaron bien los triangulos
        self.assertEqual(self.T.triangles[0], Triangle(0, 1, 8))
        self.assertEqual(self.T.triangles[6], Triangle(1, 2, 8))
        self.assertEqual(self.T.triangles[7], Triangle(2, 0, 8))
        # revisamos que tengan bien asignados sus vecinos
        self.assertEqual(self.T.triangles[0].get_vecino_opuesto(0), self.T.triangles[6])
        self.assertEqual(self.T.triangles[0].get_vecino_opuesto(1), self.T.triangles[7])
        self.assertEqual(self.T.triangles[0].get_vecino_opuesto(2), self.T.triangles[2])    # t5
        # revisamos que tengan bien asignados sus vecinos
        self.assertEqual(self.T.triangles[6].get_vecino_opuesto(0), self.T.triangles[7])
        self.assertEqual(self.T.triangles[6].get_vecino_opuesto(1), self.T.triangles[0])
        self.assertEqual(self.T.triangles[6].get_vecino_opuesto(2), self.T.triangles[5])    # t2
        # revisamos que tengan bien asignados sus vecinos
        self.assertEqual(self.T.triangles[7].get_vecino_opuesto(0), self.T.triangles[0])
        self.assertEqual(self.T.triangles[7].get_vecino_opuesto(1), self.T.triangles[6])
        self.assertEqual(self.T.triangles[7].get_vecino_opuesto(2), self.T.triangles[3])     # t4
        # revisamos que el resto tambien queden con sus vecinos bien asignados
        self.assertEqual(self.T.triangles[5].get_vecino_opuesto(2), self.T.triangles[6])
        self.assertEqual(self.T.triangles[5].get_vecino_opuesto(0), self.T.triangles[1])
        self.assertEqual(self.T.triangles[5].get_vecino_opuesto(1), self.T.triangles[4])
        self.assertEqual(self.T.triangles[3].get_vecino_opuesto(0), self.T.triangles[7])
        self.assertEqual(self.T.triangles[3].get_vecino_opuesto(2), None)
        self.assertEqual(self.T.triangles[3].get_vecino_opuesto(1), None)
        self.assertEqual(self.T.triangles[2].get_vecino_opuesto(2), self.T.triangles[0])
        self.assertEqual(self.T.triangles[2].get_vecino_opuesto(0), None)
        self.assertEqual(self.T.triangles[2].get_vecino_opuesto(1), None)
        # probamos con t6 un triangulo en el borde
        p6 = point(2.41022,-1.47037)
        self.assertEqual(self.T.triangles[1], self.t6)
        self.T.insert3(self.T.triangles[1], p6)
        # vemos si se agrego el punto a la lista de puntos
        self.assertEqual(self.T.points[9], p6)
        self.assertEqual(self.T.cnt, 10)
        # comprobamos que se generaron bien los triangulos
        self.assertEqual(self.T.triangles[1], Triangle(7, 3, 9))
        self.assertEqual(self.T.triangles[8], Triangle(3, 1, 9))
        self.assertEqual(self.T.triangles[9], Triangle(1, 7, 9))
        self.assertEqual(self.T.triangles[1].get_vecino_opuesto(0), self.T.triangles[8])
        self.assertEqual(self.T.triangles[1].get_vecino_opuesto(1), self.T.triangles[9])
        self.assertEqual(self.T.triangles[1].get_vecino_opuesto(2), None)
        self.assertEqual(self.T.triangles[8].get_vecino_opuesto(0), self.T.triangles[9])
        self.assertEqual(self.T.triangles[8].get_vecino_opuesto(1), self.T.triangles[1])
        self.assertEqual(self.T.triangles[8].get_vecino_opuesto(2), self.t2)
        self.assertEqual(self.T.triangles[9].get_vecino_opuesto(0), self.T.triangles[1])
        self.assertEqual(self.T.triangles[9].get_vecino_opuesto(1), self.T.triangles[8])
        self.assertEqual(self.T.triangles[9].get_vecino_opuesto(2), None)

    def test_insert4(self):
        p = point(1,0)
        # insertamos un punto en la arista que comparte t1 y t2.
        # Los triangulos quedan ta, t2, tb, t4 en las posiciones, 0, 6, 5, 7, respectivamente
        self.T.insert4(self.T.triangles[0], self.T.triangles[5], p)
        # vemos si se agrego el punto a la lista de puntos
        self.assertEqual(self.T.points[8], p)
        self.assertEqual(self.T.cnt, 9)
        # comprobamos que modifico el objeto y no solo la lista  
        self.assertEqual(self.t1, self.T.triangles[0])
        self.assertEqual(self.t2, self.T.triangles[5])
        # comprobamos que se generaron bien los triangulos
        self.assertEqual(self.T.triangles[0], Triangle(0, 1, 8))
        self.assertEqual(self.T.triangles[6], Triangle(1, 3, 8))
        self.assertEqual(self.T.triangles[5], Triangle(3, 2, 8))
        self.assertEqual(self.T.triangles[7], Triangle(2, 0, 8))
        # revisamos que tengan bien asignados sus vecinos ta
        self.assertEqual(self.T.triangles[0].get_vecino_opuesto(0), self.T.triangles[6])
        self.assertEqual(self.T.triangles[0].get_vecino_opuesto(1), self.T.triangles[7])
        self.assertEqual(self.T.triangles[0].get_vecino_opuesto(2), self.T.triangles[2])    # t5
        # revisamos que tengan bien asignados sus vecinos t2
        self.assertEqual(self.T.triangles[6].get_vecino_opuesto(0), self.T.triangles[5])
        self.assertEqual(self.T.triangles[6].get_vecino_opuesto(1), self.T.triangles[0])
        self.assertEqual(self.T.triangles[6].get_vecino_opuesto(2), self.T.triangles[1])    # t6
        # revisamos que tengan bien asignados sus vecinos tb 
        self.assertEqual(self.T.triangles[5].get_vecino_opuesto(0), self.T.triangles[7])
        self.assertEqual(self.T.triangles[5].get_vecino_opuesto(1), self.T.triangles[6])    
        self.assertEqual(self.T.triangles[5].get_vecino_opuesto(2), self.T.triangles[4])    # t3
        # revisamos que tengan bien asignados sus vecinos t4
        self.assertEqual(self.T.triangles[7].get_vecino_opuesto(0), self.T.triangles[0])
        self.assertEqual(self.T.triangles[7].get_vecino_opuesto(1), self.T.triangles[5])
        self.assertEqual(self.T.triangles[7].get_vecino_opuesto(2), self.T.triangles[3])    # t4
        # revisamos que el resto tambien queden con sus vecinos bien asignados
        self.assertEqual(self.T.triangles[2].get_vecino_opuesto(2), self.T.triangles[0])    # t5
        self.assertEqual(self.T.triangles[2].get_vecino_opuesto(0), None)
        self.assertEqual(self.T.triangles[2].get_vecino_opuesto(1), None)
        self.assertEqual(self.T.triangles[1].get_vecino_opuesto(0), self.T.triangles[6])    # t6
        self.assertEqual(self.T.triangles[1].get_vecino_opuesto(1), None)
        self.assertEqual(self.T.triangles[1].get_vecino_opuesto(2), None)
        self.assertEqual(self.T.triangles[4].get_vecino_opuesto(1), self.T.triangles[5])    # t3
        self.assertEqual(self.T.triangles[4].get_vecino_opuesto(0), None)
        self.assertEqual(self.T.triangles[4].get_vecino_opuesto(2), None)
        self.assertEqual(self.T.triangles[3].get_vecino_opuesto(0), self.T.triangles[7])    # t4
        self.assertEqual(self.T.triangles[3].get_vecino_opuesto(1), None)
        self.assertEqual(self.T.triangles[3].get_vecino_opuesto(2), None)

    def test_legalize_edge(self):
        # realizamos una insercion en t1
        p1 = point(0.3,-0.1)
        self.T.insert3(self.T.triangles[0], p1)
        # legalizamos el triangulo colindante con t2
        indice = self.T.triangles[6].vertices.index(self.T.cnt-1)   # indice del punto insertado en los vertices del trianglo numero 6 de la triangulacion
        
        self.T.legalize_edge(self.T.triangles[6], self.T.triangles[6].get_vecino_opuesto(self.T.triangles[6].vertices.index(self.T.cnt-1)))
        # deberia hacer flip y a los nuevos triangulos opuestos a p1 no hacer flip
        self.assertEqual(self.T.triangles[6], Triangle(1, 3, 8))
        self.assertEqual(self.T.triangles[5], Triangle(3,2, 8))
        # revisamos que el resto de los triangulos esten bien
        self.assertEqual(self.T.triangles[1], Triangle(1, 7, 3))
        self.assertEqual(self.T.triangles[1].get_vecino_opuesto(0), self.T.triangles[6])    # t6
        self.assertEqual(self.T.triangles[1].get_vecino_opuesto(1), None)
        self.assertEqual(self.T.triangles[1].get_vecino_opuesto(2), None)
        self.assertEqual(self.T.triangles[4].get_vecino_opuesto(0), None)    # t3
        self.assertEqual(self.T.triangles[4].get_vecino_opuesto(1), self.T.triangles[5])
        self.assertEqual(self.T.triangles[4].get_vecino_opuesto(2), None)
        self.assertEqual(self.T.triangles[5].get_vecino_opuesto(0), self.T.triangles[7])    # t2
        self.assertEqual(self.T.triangles[5].get_vecino_opuesto(1), self.T.triangles[6])
        self.assertEqual(self.T.triangles[5].get_vecino_opuesto(2), self.T.triangles[4])
        self.assertEqual(self.T.triangles[6].get_vecino_opuesto(0), self.T.triangles[1])    # t11
        self.assertEqual(self.T.triangles[6].get_vecino_opuesto(1), self.T.triangles[5])    
        self.assertEqual(self.T.triangles[6].get_vecino_opuesto(2), self.T.triangles[0])
        # legalizamos el triangulo colindante con t5
        self.T.legalize_edge(self.T.triangles[0], self.T.triangles[0].get_vecino_opuesto(self.T.triangles[0].vertices.index(self.T.cnt-1)))
        # deberia hacer flip
        self.assertEqual(self.T.triangles[0], Triangle(0, 6, 8))
    
    def test_point_on_edge(self):
        self.assertEqual( self.T.point_on_edge(point(1,0), self.T.triangles[0]),(True,0))
        _,i = self.T.point_on_edge(point(1,0), self.T.triangles[0])
        self.assertEqual(self.T.triangles[0].get_vecino_opuesto(i),self.T.triangles[5])
        self.assertEqual( self.T.point_on_edge(point(1,0), self.T.triangles[5]),(True,2))
        _,i = self.T.point_on_edge(point(1,0), self.T.triangles[5])
        self.assertEqual(self.T.triangles[5].get_vecino_opuesto(i),self.T.triangles[0])
        self.assertEqual( self.T.point_on_edge(point(1,3), self.T.triangles[1]),(False,None))

    def test_triangulate(self):
        # creo un objeto nuevo
        T2 = Triangulation(1e-10)
        # puntos
        ps = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]
        T2.triangulate(ps)
        print(T2.triangles)
        print(T2.points)
if __name__ == '__main__':
    unittest.main()
