# Ejercicio 2
from math       import log
from numpy      import linspace
from matplotlib import pyplot


""" Método de Newton """
def rnewton(fun, x0, err, mit):
    """ fun:  es una función que dado x, retorna f(x), f'(x) 
        x0:   es el punto inicial
        err:  es la tolerancia deseada
        mit:  es el número de iteraciones permitido
    """
    hx,hf = [],[]
    
    x_prev = x0
    f,fp = fun(x_prev)
    
    if fp == 0:
        print("[rnewton] La derivada se nula en x0 == {}\n".format(x0))
        return hx, hf
    
    hx.append(x_prev)
    hf.append(f)

    it = 1    
    while it <= mit and abs(f) >= err:
        x_sig = x_prev - (f/fp)
        
        e = abs(x_sig - x_prev) / abs(x_sig)
        if e < err:
            print("[rnewton] Puntos relativamente muy cercanos\n")
            print("[rnewton] Lo último que se calculo fue f({}) ~ {}\n".format(x_prev, f))
            return hx,hf
        
        x_prev = x_sig
        f,fp = fun(x_prev)
        if fp == 0:
            print("[rnewton] La derivada se nula en x0 == {}\n".format(x0))
            return hx, hf
        
        hx.append(x_prev)
        hf.append(f)
        
        it += 1
    if abs(f) < err:
        print("[rnewton] Converge por f({}) ~ {}\n".format(x_prev, f))
        print("[rnewton] Converge a las {} iteraciones (de {} iteraciones dadas).\n".format(it, mit))
    
    return hx,hf


""" Dado x, devuelve (f(x), f'(x) )
    Observar que la solución de f(x) se da por
    f(x) == 0
    log(x) - 1/x == 0
    x*log(x) == 1
    log(x**x) == 1
    Lo que implica que x**x == e
"""
def funcion_ejercicio(x):
    return ( log(x) - 1/x, 1/x + 1/(x**2) )


""" Inciso a) """
def inciso_a():
    x0  = 1.4
    mit = 100
    tol = 1e-6
    res = rnewton(funcion_ejercicio, x0, tol, mit)[0][-1]
    f_res = funcion_ejercicio(res)[0]
    if f_res < tol:
        print("La raíz de 'f(x) = log(x) - 1/x' por rnewton es %s\n\n"%res)
        return res
    else:
        print("El último punto evaluado (%s) no cumple la tolerancia dada (f(%s) == %s >= %s)\n"%(res, res, f_res, tol))
        print("Podría intentarse con otro punto inicial (x0)\n\n")
        return None


""" Inciso b): Método de Steffensen """
def rsteff(fun, x0, err, mit):
    """ fun:  es una función que dado x, retorna f(x), f'(x) 
        x0:   es el punto inicial
        err:  es la tolerancia deseada
        mit:  es el número de iteraciones permitido
    """
    hx,hf = [],[]

    x_prev = x0
    f = fun(x_prev)[0]
    
    hx.append(x_prev)
    hf.append(f)
    
    it = 1
    while it <= mit and abs(f) >= err:
        denominador = fun( x_prev + f)[0] - f
        if denominador == 0:
            print("[rsteff] El denominador se anula en {}\n".format(x_prev + f))
            print("[rsteff] Lo último que se calculo fue f({}) ~ {}\n".format(x_prev, f))
            return hx,hf
        
        x_sig = x_prev - (f**2/denominador)
        
        e = abs(x_sig - x_prev) / abs(x_sig)
        if e < err:
            print("[rsteff] Puntos relativamente muy cercanos\n")
            print("[rsteff] Lo último que se calculo fue f({}) ~ {}\n".format(x_prev, f))
            return hx,hf
        
        x_prev = x_sig
        f = fun(x_prev)[0]
        
        hx.append(x_prev)
        hf.append(f)
        
        it += 1
    
    if abs(f) < err:
        print("[rsteff] Converge por f({}) ~ {}\n".format(x_prev, f))
        print("[rsteff] Converge a las {} iteraciones (de {} iteraciones dadas).\n".format(it, mit))
    
    return hx, hf


""" Inciso c): Comparación de métodos en puntos distintos

    Ambos métodos encuentran aproximadamente la raíz de la
    función pedida, en este caso.
    Ambos métodos tienen convergencia cuádratica hasta donde
    sé, aunque las condiciones son distintas, pues Steffensen
    usa una aproximación de la derivada en cada paso (se parecen
    cuando la diferencia entre la función en un punto es cercano al
    punto, algo que se puede ver por la forma del cociente 
    incremental).
    Por lo anterior, Steffensen no se salva de la operación
    extra que se da como en el método de Newton, respecto a
    la derivada (se hace una evaluación para el denominador).
    Ambos métodos requieren un punto inicial, algo muy
    cómodo a diferencia de los métodos de Bisección o de la 
    Secante.
    Así mismo, como para Steffensen no es necesaria la derivada
    de la función con la que se está trabajando nos ahorramos
    el trabajo de hacer un calculo posiblemente complicado.
"""
def inciso_c():
    puntos_visualizacion = linspace(0.8, 5, 2000)
    
    puntos_testeo = [1.39, 1.40, 1.41, 3]
    
    tol = 1e-6
    mit = 100
    
    x_rnewton  = []
    fx_rnewton = []
    
    x_rsteff  = []
    fx_rsteff = []
    
    """ En este caso, aunque no se hace notar mucho la diferencia, Steffensen
        requiere más iteraciones que Newton para cada punto inicial
        Parece que con Steffensen se agrupan mas los puntos de convergencia
        respecto a la tolerancia dada
    """
    for x0 in puntos_testeo:
        hx,hf = rnewton(funcion_ejercicio, x0, tol, mit)
        x_rnewton.append( hx[-1] )
        fx_rnewton.append( hf[-1] )
    
    for x0 in puntos_testeo:
        hx,hf = rsteff(funcion_ejercicio, x0, tol, mit)
        x_rsteff.append( hx[-1] )
        fx_rsteff.append( hf[-1] )
        
    """ No se va a notar la diferencia """
    pyplot.plot(x_rsteff, fx_rsteff, "ob", label="Convergencia rsteff")
    pyplot.plot(x_rnewton, fx_rnewton, "or", label="Convergencia rnewton")
    
    """ Graficamos la función """
    pyplot.plot(puntos_visualizacion, list(map(lambda  x : log(x) - 1/x, puntos_visualizacion)), "g", label="$f(x) = log(x) - 1/x$")
    
    pyplot.title("Ejercicio 2, inciso c)")
    pyplot.legend(loc="upper left")
    pyplot.axhline(0, color='black')
    pyplot.axvline(0, color='black')
    pyplot.show()
