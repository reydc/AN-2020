from importlib  import reload
from matplotlib import pyplot
from numpy      import linspace, loadtxt, arcsin, cos, log, exp, pi
from numpy.random import seed, randn
from numpy.polynomial.polynomial import polyfit, polyval

""" Ejercicio 1 """

""" Devuelve los coeficientes de un ajuste lineal,
    donde obtenemos la recta y = a * x + b
"""
def ajuste_lineal(x, y):
    sum_x   = sum( [ p_x for p_x in x ] )
    sum_x_x = sum( [ p_x * p_x for p_x in x ] )
    sum_y   = sum( [ p_y for p_y in y ] )
    sum_x_y = sum( [ x[i]* y[i] for i in range(len(x)) ] )
    
    denominador = len(x) * sum_x_x - sum_x * sum_x
       
    b = sum_x_x * sum_y - sum_x_y * sum_x
    b /= denominador
    
    a = len(x) * sum_x_y  - sum_x * sum_y
    a /= denominador
    
    return [b, a]

def ej1a():
    data = loadtxt(fname="Datos_Laboratorio_4/datos1a.dat", encoding="ascii")
    
    b, a = ajuste_lineal(data[0], data[1])
    
    min_x, max_x = min(data[0]), max(data[0])
    
    puntos_recta = linspace(min_x, max_x, 100)
    
    pyplot.plot(data[0], data[1], "*r", label="Pares")
    pyplot.plot(puntos_recta, list(map(lambda x : a*x + b, puntos_recta)), "g", label="Recta de ajuste")
    pyplot.title("Ejercicio 1.a")
    pyplot.legend(loc="upper left")
    pyplot.axhline(0, color='black')
    pyplot.axvline(0, color='black')
    
    pyplot.show()

def ej1b():
    
    seed()
    """ Lo que se quiere es perturbar los y """
    x = linspace(0,10,20)
    y = 3/4 * x - 1/2 + randn(20)
    
    b, a   = ajuste_lineal(x, y)
    
    c = polyfit(x, y, deg=1)
    
    print("Recta de ajuste lineal [ajuste_lineal], con:")
    print("pendiente = %s"%a)
    print("constante = %s"%b)
    print("y_aprox   = %s * x + (%s)"%(a, b))
    
    print("Recta de ajuste lineal [polyfit], con:")
    print("pendiente = %s"%c[1])
    print("constante = %s"%c[0])
    print("y_aprox'  = %s * x + (%s)"%(c[1], c[0]))
    
    fig, plots = pyplot.subplots(1, 2)
    fig.suptitle("Ejercicio 1.b", ma="center")
    plots[0].plot(x, y, "*r", label="Pares")
    plots[0].plot(x, a*x + b, "g", label="Recta de ajuste")
    plots[0].plot(x, 3/4 * x - 1/2, color="orange" , label="Recta Original")
    plots[1].plot(x, y, "*r", label="Pares")
    plots[1].plot(x, polyval(x, c), "b", label="Polyfit")
    plots[1].plot(x, 3/4 * x - 1/2, color="orange" , label="Recta Original")
    plots[0].legend(loc="upper left")
    plots[1].legend(loc="upper left")
    plots[0].axhline(0, color='black')
    plots[0].axvline(0, color='black')
    plots[1].axhline(0, color='black')
    plots[1].axvline(0, color='black')
    
    pyplot.show()

""" Ejercicio 2 """

def ej2a():
    x = linspace(0, 1, 50)
    y = arcsin(x)
    
    fig, plots = pyplot.subplots(2, 3)
    fig.suptitle("Ejercicio 2.a", ma="center")
    
    for n in range(6):
        i = n // 3
        j = n % 3
        
        c = polyfit(x, y, deg=n)
        plots[i,j].plot(x, y, "*r", label="Pares (x,y)")
        plots[i,j].plot(x, polyval(x, c), "g", label="$P_%s(x)$"%n)
        plots[i,j].legend(loc="upper left")
        plots[i,j].axhline(0, color="black")
        plots[i,j].axvline(0, color="black")
    
    pyplot.show()

def ej2b():
    x = linspace(0, 4*pi, 50)
    y = cos(x)

    fig, plots = pyplot.subplots(2, 3)
    fig.suptitle("Ejercicio 2.b", ma="center")

    for n in range(6):
        i = n // 3
        j = n % 3
        
        c = polyfit(x, y, deg=n)
        plots[i,j].plot(x, y, "*r", label="Pares (x,y)")
        plots[i,j].plot(x, polyval(x, c), "g", label="$P_%s(x)$"%n)
        plots[i,j].legend(loc="upper left")
        plots[i,j].axhline(0, color="black")
        plots[i,j].axvline(0, color="black")

    pyplot.show()

def ej3a():
    data = loadtxt(fname="Datos_Laboratorio_4/datos3a.dat", encoding="ascii")
    
    """ Se nos da y = C*x**A, que tomando logaritmos es log(y) = log(C) + A * log(x)
        Entonces ajustamos y' = log(y), x' = log(x)
    """

    l_x = [ log(x) for x in data[0]]
    l_y = [ log(y) for y in data[1]]
    
    c = polyfit(l_x, l_y, deg=1)
    A = c[1]
    C = exp(c[0])
    print("Ejercicio 3.a: y = C*(x**A)")
    print("C = %s"%C)
    print("A = %s"%A)
    
    I = linspace(min(data[0]), max(data[0]), 1000)

    pyplot.plot(data[0], data[1], "*r", label="Datos")
    pyplot.plot(I, C*(I**A), "g", label="$\\tilde{y}(x) = %sx^{%s}$"%(C,A))
    pyplot.plot(l_x, l_y, "*", color="orange", label="Datos de ajuste (pares de log)")
    pyplot.plot(l_x, polyval(l_x, c), "b", label="$log(y) = (%s) + (%s)x$"%(c[1],c[0]))
    pyplot.title("Ejercicio 3.a")
    pyplot.legend(loc="upper left")
    pyplot.show()
    return C, A

def ej3b():
    data = loadtxt(fname="Datos_Laboratorio_4/datos3b.dat", encoding="ascii")
    
    """ Se nos da y = x / (A*x + B), de donde tenemos
        y = 1 / (A + B * (1/x))
        A + B * (1/x) = 1/y
        Entonces debemos ajustar
        y' = 1/y
        x' = 1/x
    """
    x = 1 / data[0,1:]
    y = 1 / data[1,1:]
    c = polyfit(x, y, deg=1)
    A = c[0]
    B = c[1]
    print("Ejercicio 3.b: y = x / (A * x + B)")
    print("B = %s"%B)
    print("A = %s"%A)
    
    I = linspace(min(data[0,1:]), max(data[0,1:]), 1000)

    pyplot.plot(data[0], data[1], "*r", label="Datos")
    pyplot.plot(I, I/(A * I + B), "g", label="$\\tilde{y}(x) = \\frac{x}{(%s)x + (%s)}$"%(A,B))
    pyplot.plot(x, y, "*", color="orange", label="Datos de ajuste ($\\frac{1}{y}$)")
    pyplot.plot(x, polyval(x, c), "b", label="$\\frac{1}{y} = (%s)\\frac{1}{x} + (%s)$"%(B,A))
    pyplot.title("Ejercicio 3.a")
    pyplot.legend(loc="upper left")
    pyplot.axhline(0, color="black")
    pyplot.axvline(0, color="black")
    
    pyplot.show()
    
    return A, B

""" Ejercicio 4 """

def ej4():
    data = loadtxt("Datos_Laboratorio_4/covid_italia.csv", delimiter=",", encoding="ascii")
    n, _ = data.shape
    """ Sea y = a*(e**(b*x)) el módelo a ajustar. Entonces tenemos
        log(y) = log(a) + b * x, es decir y' = log(y), x' = x
    """
    x = [ data[i][0] for i in range(n)]
    y = [ data[i][1] for i in range(n)]
    l_y = log(y)
    c = polyfit(x, l_y, deg=1)
    a = exp(c[0])
    b = c[1]
    print("Ejercicio 4: y = a*(e**(b*x))")
    print("a = %s"%a)
    print("b = %s"%b)
    
    I = linspace(min(x), max(x), 1000)
    
    pyplot.plot(x, y, "*r", label="Datos")
    pyplot.plot(x, l_y, "*", color="orange", label="Datos de ajuste")
    pyplot.plot(I, a*exp(b*I), "g", label="$\\tilde{y}(x) = %se^{%sx}$"%(a,b))
    pyplot.plot(x, polyval(x, c), "b", label="Recta de ajuste")
    pyplot.title("Ejercicio 4")
    pyplot.ylim(-20000, max(y))
    pyplot.legend(loc="upper left")
    pyplot.axhline(0, color="black")
    pyplot.axvline(0, color="black")
    
    pyplot.show()

    return a, b
