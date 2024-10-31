from point import point
import numpy as np

# Orient2D
# Determina la orientacion de p respecto a la arista de los puntos (en sentido antihorario) b y c.
#  Retorna 1 si esta dentro, 0 si esta en la arista o es colineal y -1 si esta afuera
# Recibe los puntos y un epsilon para indicar la tolerancia 
def orient2d(p, b, c, epsilon) -> int:
    det = (b.x - p.x) * (c.y - p.y) - (b.y - p.y) * (c.x - p.x)
    if abs(det) < epsilon:
        return 0 
    elif det > 0:
        return 1  # Dentro
    else:
        return -1  # Fuera
    
# InCirecle
# Determina si un punto x esta en el circuncirlculo formado por los puntos abc del triangl
def incircle(p,a,b,c, epsilon):
        """Check if point p is inside of circumcircle around the triangle tri.
        This is a robust predicate, slower than compare distance to centers
        ref: http://www.cs.cmu.edu/~quake/robust.html
        """
        tri = [np.array((a.x, a.y)), np.array((b.x, b.y)), np.array((c.x, c.y))]
        q = np.array((p.x, p.y))
        m1 = np.asarray([v - q for v in tri])
        m2 = np.sum(np.square(m1), axis=1).reshape((3, 1))
        m = np.hstack((m1, m2))    # The 3x3 matrix to check
        det = np.linalg.det(m)
    
        # Evaluar con EPSILON para manejar errores numéricos
        if abs(det) < epsilon:
            return 0  # El punto está en el círculo
        elif det > 0:
            return 1  # El punto está dentro del círculo
        else:
            return -1  # El punto está fuera del círculo
        

