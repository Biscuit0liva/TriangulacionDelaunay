from point import point

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
def incircle(p,a, b, c, epsilon):
    # Determinante extendido para InCircle2D
    det = (
        (p.x * p.x + p.y * p.y) * ((a.x * (b.y - c.y)) + (b.x * (c.y - a.y)) + (c.x * (a.y - b.y)))
        - (p.y * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)))
        + (a.x * a.x + a.y * a.y) * ((b.x * (c.y - p.y)) + (c.x * (p.y - b.y)) + (p.x * (b.y - c.y)))
        - (a.y * (b.x * (c.y - p.y) + c.x * (p.y - b.y) + p.x * (b.y - c.y)))
        + (b.x * b.x + b.y * b.y) * ((c.x * (p.y - a.y)) + (p.x * (a.y - c.y)) + (a.x * (c.y - p.y)))
        - (b.y * (c.x * (p.y - a.y) + p.x * (a.y - c.y) + a.x * (c.y - p.y)))
        + (c.x * c.x + c.y * c.y) * ((p.x * (a.y - b.y)) + (a.x * (b.y - p.y)) + (b.x * (p.y - a.y)))
        - (c.y * (p.x * (a.y - b.y) + a.x * (b.y - p.y) + b.x * (p.y - a.y)))
    )
    
    # Evaluar con EPSILON para manejar errores numéricos
    if abs(det) < epsilon:
        return 0  # El punto está en el círculo
    elif -det > 0:
        return 1  # El punto está dentro del círculo
    else:
        return -1  # El punto está fuera del círculo
