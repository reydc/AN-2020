# Ejercicio 1
from matplotlib        import pyplot
from scipy.interpolate import CubicSpline
import numpy as np

""" Para ver lo que se obtiene de la siguiente tabla ejecutar interactivamente:
    ej1.ejercicio1()
"""
t_s = np.array([0., 0.22, 0.85 , 1.   , 1.5 , 1.6 , 1.99])
v_s = np.array([0., 0.1 , -0.15, -0.03, 0.75, -0.3, 0.01])

""" Ejercicio 1.a
    Consideramos dada una tabla de pares (tiempo [s], velocidad [m/s]).
    Se pide implementar spline_velocidad.
"""
def spline_velocidad(ts, vs):
    """ spline_velocidad:

        Recibe ts, vs:
        
        ts: Lista o numpy.array unidimensional con los tiempos de la tabla en orden.

        vs: Lista o numpy.array unidimensional con las velocidades de la tabla en orden.

        Devuelve par de listas t, v:

        t:  Lista que contiene todos los puntos de la lista de entrada ts y los puntos
            medios entre dos puntos consecutivos.

        v:  Lista con los puntos de evaluación de un spline cúbico de la función 
            velocidad en los puntos de la nueva partición.
        
        Ejemplo:
        
        ej1.spline_velocidad(ej1.t_s, ej1.v_s)
    """
    t = []
    ts_prima = ts
    n = len(ts_prima)
    for i in range(n):
        if i < n - 1:
            t.append( ts_prima[i] )
            t.append( (ts_prima[i] + ts_prima[i + 1]) / 2)
        else:
            t.append( ts_prima[i] )

    v = list(CubicSpline(ts, vs)(t))
    
    return t, v

""" Ejercico 1.b
    Se pide implementar trapecio_adaptativo.
"""
def trapecio(a, b, f_a, f_b):
    """ trapecio:
        
        Regla básica del trapecio para usar en dos puntos y aproximar la integral
        de f(x) entre dos puntos a y b.
        
        Recibe a, b, f_a, f_b:
        
        a: Límite inferior de la integral.
        
        b: Límite superior de la integral.
        
        f_a: Valor de f(a)
        
        f_b: Valor de f(b)
        
        Devuelve el valor aproximado de la integral de f(x) entre a y b. 
    """
    return (b - a) * (f_a + f_b) / 2


def trapecio_adaptativo(x, y):
    """ trapecio_adaptativo:

        Versión modificada de la regla del trapecio para integrar en intervalos de 
        longitud arbitraria (no equidistantes).
        
        Recibe xs, ys:
        
        x: Lista o numpy.array unidimensional con los puntos de evaluación en 
           orden.
        
        y: Lista o numpy.array unidimensional con los valores en los puntos de
           evaluación dados en x en orden.
        
        Devuelve el valor aproximado de la integral por la regla del trapecio
        adaptativo usando los límites dados por x.
        
        Ejemplo:
        
        ej1.trapecio_adaptativo( ej1.spline_velocidad(ej1.t_s, ej1.v_s) )
    """
    n = len(x)
    if n != len(y):
        print("Las entradas x e y tienen distinta longitud.\n")
        return None
    
    return sum([ trapecio(x[i], x[i + 1], y[i], y[i + 1]) for i in range(n - 1)])

""" Ejercicio 1.c
    Aproximar la posición de la partícula en todos los instantes de tiempo de la 
    nueva partición, sabiendo que se encuentra en la posición x = 0 en el instante 
    t = 0. Para eso es necesario integrar la función de velocidad desde 0 hasta
    cada punto de la partición. Si x es la posición y t el tiempo:
    velocidad = dx / dt
    implica
    integral(0, t_val) velocidad(t) dt = x(t_val)
    Nosotros tenemos la tabla:
    | tiempo    [s]   |
    | velocidad [m/s] |
    Se pide graficar las posiciones.
"""
def posicion_particula(ts, vs):
    """ posición_particula:

        Toma los datos necesarios para resolver dar las posiciones de las 
        partículas y graficae la función de posición de la partícula. 
        El trabajo se hace directamente, es decir, calcula, después grafica, y 
        al cerrar el gráfico devuelve los valores calculados en el orden dado
        por el tiempo.
        
        Recibe ts, vs:
        
        ts: Lista o numpy.array unidimensional con los tiempos de la tabla en orden.
        
        vs: Lista o numpy.array unidimensional con las velocidades de la tabla en orden.
        
        Devuelve x:
        
        x: Lista de posiciones en el tiempo correspondiente a los dados por ts.
        
        Ejemplo:
        
        ej1.posicion_particula(ej1.t_s, ej1.v_s)
    """
    t, v = spline_velocidad(ts, vs)
    n = len(t)
    x   = []
    for i in range(1, n + 1):
        x.append( trapecio_adpatativo(t[:i], v[:i]) )
    
    pyplot.plot(t, x, label = "Posiciones")
    pyplot.title("Ejercicio 1")
    pyplot.ylabel("x")
    pyplot.xlabel("t")
    pyplot.legend(loc="upper left")
    pyplot.axhline(0, color="black")
    pyplot.axvline(0, color="black")
    pyplot.show()

    return x

def ejercicio1():
    """ Muestra la solución del problema para la tabla dada en la consigna """
    posicion_particula(t_s, v_s)
