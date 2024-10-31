import unittest
import sys
import os

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from point import point
from Triangle import Triangle
from Edge import Edge

class TestTriangle(unittest.TestCase):
    def test_creacion_triangulo(self):
        p1 = point(0, 0)
        p2 = point(1, 0)
        p3 = point(0, 1)
        ps = [p3,p2,p1]
        tri = Triangle(2, 1, 0)
        
        # Verifica que los vértices estén correctamente asignados
        self.assertEqual(ps[tri.vertices[0]], p1)
        self.assertEqual(ps[tri.vertices[1]], p2)
        self.assertEqual(ps[tri.vertices[2]], p3)
    
    def test_get_arista_opuesta(self):
        p1 = point(0, 0)
        p2 = point(1, 0)
        p3 = point(0, 1)
        ps = [p1,p2,p3]
        tri = Triangle(0, 1, 2)
        
        # Verificar que get_arista devuelve los puntos correctos
        arista = tri.get_arista_opuesta(0)
        self.assertEqual(arista, (1, 2))  # La arista opuesta a p1
        arista = tri.get_arista_opuesta(1)
        self.assertEqual(arista, (2, 0))  # La arista opuesta a p2
        arista = tri.get_arista_opuesta(2)
        self.assertEqual(arista, (0, 1))  # La arista opuesta a p2

    def test_set_vecinos(self):
        # puntos
        a = point(0, 0)
        b = point(1, -1)
        c = point(1, 1)
        d = point(2, 0)
        e = point(2, 1)
        f = point(-1, 1)
        g = point(0, -2)
        h = point(3, -2)
        ps = [a, b, c, d, e, f, g, h]
        # triangulos de prueba, se crean con los indices de los puntos en ps
        t1 = Triangle(0, 1, 2)
        t2 = Triangle(2, 1, 3)
        t3 = Triangle(3, 4, 2)
        t4 = Triangle(5, 0, 2)
        t5 = Triangle(1, 0, 6)
        t6 = Triangle(7, 3, 1)

        # seteamos sus vecinos
        t1.set_vecino(0, t2)
        t1.set_vecino(1, t4)
        t1.set_vecino(2, t5)
        t2.set_vecino(0, t6)
        t2.set_vecino(1, t3)
        t2.set_vecino(2, t1)
        t3.set_vecino(1, t2)
        t4.set_vecino(0, t1)
        t5.set_vecino(2, t1)
        t6.set_vecino(0, t2)
        # revisamos que quedan bien referenciados los vecinos
        self.assertEqual(t1.vecinos[0], t2)
        self.assertEqual(t1.vecinos[1], t4)
        self.assertEqual(t1.vecinos[2], t5)
        self.assertEqual(t2.vecinos[0], t6)
        self.assertEqual(t2.vecinos[1], t3)
        self.assertEqual(t2.vecinos[2], t1)
        self.assertEqual(t3.vecinos[0], None)
        self.assertEqual(t3.vecinos[1], t2)
        self.assertEqual(t3.vecinos[2], None)
        self.assertEqual(t4.vecinos[0], t1)
        self.assertEqual(t4.vecinos[1], None)
        self.assertEqual(t4.vecinos[2], None)
        self.assertEqual(t5.vecinos[0], None)
        self.assertEqual(t5.vecinos[1], None)
        self.assertEqual(t5.vecinos[2], t1)
        self.assertEqual(t6.vecinos[0], t2)
        self.assertEqual(t6.vecinos[1], None)
        self.assertEqual(t6.vecinos[2], None)

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
        t1.replace(t2, t3)
        t1.replace(t5, t2)
        self.assertEqual(t1.vecinos[1], t6)
        self.assertEqual(t1.vecinos[0], t3)
        self.assertEqual(t1.vecinos[2], t2)

    def test_is_intersected(self):
        # puntos
        a = point(0, 0)
        b = point(1, -1)
        c = point(1, 1)
        d = point(2, 0)
        e = point(2, 1)
        f = point(-1, 1)
        g = point(0, -2)
        h = point(3, -2)
        ps = [a, b, c, d, e, f, g, h]
        # triangulos de prueba, se crean con los indices de los puntos en ps
        t1 = Triangle(0, 1, 2)
        t2 = Triangle(2, 1, 3)
        t3 = Triangle(3, 4, 2)
        t4 = Triangle(5, 0, 2)
        t5 = Triangle(1, 0, 6)
        t6 = Triangle(7, 3, 1)
        # aristas de prueba (cuando es una arista que esta inicia y termina dentro del triangulo, da falso)
        e1 = Edge(point(0,0), point(1.1, 0))
        e2 = Edge(point(0.16,0.7), point(1.44, -0.8))
        e3 = Edge(point(0.4,-0.4), point(1.32, 0.78))
        # aristas que salen de un vertice del triangulo
        e4 = Edge(point(0.41,-1.05), c)
        e7 = Edge(b,point(0.54, 1.05))
        e5 = Edge(point(-0.4614,1.7801), point(2.5, 0.5))
        e6 = Edge(point(1,-0.51), point(2.53, -0.55))   # segmento tangente en una arista
        e8 = Edge(point(1.61,0.35), point(-0.23, -0.26))
        e9 = Edge(point(0.28,0.72), point(0.1, -0.4))
        e10 = Edge(point(2.76,0.002), point(0.04, 0.22))
        self.assertTrue(t1.is_intersected(e1, ps))
        self.assertTrue(t1.is_intersected(e2, ps))
        self.assertTrue(t1.is_intersected(e3, ps))
        self.assertTrue(t1.is_intersected(e4, ps))
        self.assertTrue(t1.is_intersected(e7, ps))
        self.assertFalse(t1.is_intersected(e5, ps))
        self.assertFalse(t1.is_intersected(e6, ps))
        self.assertTrue(t1.is_intersected(e8, ps))
        self.assertTrue(t1.is_intersected(e9, ps))
        self.assertTrue(t1.is_intersected(e10, ps))

        # prueba con arista colineal a los lados de los triangulos 
        # caso bastante improbable, pero se debe considerar
        # si la arista es colineal entonces no se deberia modificar la triangulacion pues ya se respeta 
        s = point(0, 1.5)   # 0 
        t = point(0.5, 1.5) # 1
        u = point(0.14, 1.97)   # 2
        v = point(1.5, 1.5) # 3
        w = point(1, 2)    # 4
        x = point(-0.9, 1.5)   # 5
        y = point(-0.5, 1.28)   # 6
        z = point(-0.5, 2)   # 7
        ta = Triangle(0, 1, 2)  
        tb = Triangle(1,3,4)
        tc = Triangle(6,0,7)
        td = Triangle(6,7,5)
        xv = Edge(x, v)
        self.assertFalse(ta.is_intersected(xv, [s,t,u,v,w,x,y,z]))
        self.assertFalse(tb.is_intersected(xv, [s,t,u,v,w,x,y,z]))
        self.assertTrue(tc.is_intersected(xv, [s,t,u,v,w,x,y,z]))
        self.assertTrue(td.is_intersected(xv, [s,t,u,v,w,x,y,z]))

if __name__ == '__main__':
    unittest.main()
