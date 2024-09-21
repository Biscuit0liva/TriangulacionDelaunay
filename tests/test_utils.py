import unittest
import sys
import os

# Agregar el directorio raíz del proyecto a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from point import point
import utils as u

class TestUtils(unittest.TestCase):
    def test_orient2D(self):
        a = point(0,0)
        b = point(1,-1)
        c = point(1,1)
        d = point(2,0)
        f = point(1,0)
        # verifica  que a este adentro, d afuera y f en la arista bc
        self.assertEqual(u.orient2d(a, b, c, 1e-10), 1, "Adentro")
        self.assertEqual(u.orient2d(d, b, c, 1e-10), -1, "Fuera")
        self.assertEqual(u.orient2d(f, b, c, 1e-10), 0, "En")
        # prueba de robustes
        e = point(1.0000000001,0)
        self.assertEqual(u.orient2d(e, b, c, 1e-10), -1, "Fuera")
        self.assertEqual(u.orient2d(e, b, c, 1e-9), 0, "En la arista")
    
    def test_inCircle(self):
        # Definir los puntos del triángulo
        a = point(0, 0)
        b = point(1, -1)
        c = point(1, 1)
        
        # Punto p dentro del circuncírculo
        p_in = point(0.5, 0)
        # Punto p fuera del circuncírculo
        p_out = point(2.2, 0)
        # Punto p en el borde del circuncírculo
        p_on = point(2, 0)
        
        # Verificar que el punto está dentro del circuncírculo
        self.assertEqual(u.incircle(p_in, a, b, c, 1e-10), 1, "Punto dentro del circuncírculo")
        self.assertEqual(u.incircle(p_in, a, b, c, 1e-10), 1, "Punto dentro del circuncírculo")
        # Verificar que el punto está fuera del circuncírculo
        self.assertEqual(u.incircle(p_out, a, b, c, 1e-20), -1, "Punto fuera del circuncírculo")
        
        # Verificar que el punto está en el borde del circuncírculo
        self.assertEqual(u.incircle(p_on, a, b, c, 1e-10), 0, "Punto en el borde del circuncírculo")
        
        # Prueba de robustez con un punto casi en el borde
        p_almost_on = point(2.0000000001, 0)
        self.assertEqual(u.incircle(p_almost_on, a, b, c, 1e-10), -1, "Punto fuera (por poco)")
        self.assertEqual(u.incircle(p_almost_on, a, b, c, 1e-9), 0, "Punto casi en el borde")
        # prueba triangulacion
        p = point(0.3, -0.1)
        a = point(3,-2)
        b = point(2,0)
        c = point(1,-1)
        self.assertEqual(u.incircle(p, c, a, b, 1e-10), -1)
        self.assertEqual(u.incircle(p, b, c, a, 1e-10), -1)
        self.assertEqual(u.incircle(p, a, b, c, 1e-10), -1)
        a = point(1,1)
        b = point(1,-1)
        c = point(2,0)
        self.assertEqual(u.incircle(p, c, a, b, 1e-10), 1)
        self.assertEqual(u.incircle(p, a, b, c, 1e-10), 1)


if __name__ == '__main__':
    unittest.main()