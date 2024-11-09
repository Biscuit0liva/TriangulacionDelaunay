# Triangulacion de Delaunay

Proyecto  de implementacion en python de triangulacion de Delaunay utilizando el algoritmo incremental de insercion aleatoria

## Requisitos

- Pyglet
- OpenGl
- Numpy


```shell
# instalacion de requisitos del visualizador
pip install -r requirements.txt
```
## Ejecutar
Para ejecutar se tienen cuatro opciones para triangular puntos aleatorios:

- Grilla uniforme: genera puntos de una grilla con coordenadas enteras. Con x filas e y columnas
```shell
python examples/vis_m2d.py u x y
```

- Grilla uniforme aleatoria: Analoga al metodo anterior, pero elige n puntos al azar de la grilla.
```shell
python examples/vis_m2d.py ur x y n
```

- Rectangulo: genera n puntos al azar en un rectangulo de dimensiones (-a,a) (-b,b).
```shell
python examples/vis_m2d.py r a b n
```

- Circulo: genera n puntos aleatorios dentro de un circulo de radio r.
```shell
python examples/vis_m2d.py c r n
```
## Aristas restringidas
Ejecucion con aristas restringidas. En la visualizacion las aristas que se respeten estaran de color rojo. No soporta el caso de aristas que se cruzen

- Rectangulo: genera n puntos aleatorios en un rectangulo (-a,a) (-b,b) y acepta aristas restringidas a respetar

```shell
python examples/vis_m2d.py er a b n "((p1x,p1y),(p2x,p2y))" ...
```

- Arista aleatoria: Semejante al caso anterior pero genera 1 arista aleatoria que se respetara

```shell
python examples/vis_m2d.py err a b n
```

## LEPP
Para todas las ejecuciones, se tiene la funcionalidad de ir viendo el LEPP de cada triangulo en la lista de la triangulacion. Avanza en la lista con la tecla L y retrocede con K. El camino LEPP de triangulos se coloreara verde 