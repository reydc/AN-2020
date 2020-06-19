from importlib    import reload
from mpl_toolkits import mplot3d 
from matplotlib   import pyplot
from scipy        import optimize
import numpy as np

""" Ejercicio 1
    Cada Kg de fertilizante alcanza para 10 m^2 si cumple los requerimientos.
    El fertilizante debe contener al menos, por 10 m^2 (ie por Kg):
    P: 3 gr
    N: 1.5 gr
    K: 4 gr

    En el mercado hay dos tipos de fertilizantes, que podemos poner como:
    Por Kg  P     N     K      Costo
    T1      3 gr  1 gr  8 gr   10 $
    T2      2 gr  3 gr  2 gr   8 $

    Veamos los siguientes puntos:
    a. ¿Cuántos Kg de cada fertilizante se debe comprar, por cada 10 m^2 de campo,
       de modo de minimizar el costo total, bajo los requerimientos?
    Si 1 Kg de T1 cuesta 10 $, entonces 1 gr costaría 1/100 $.
    Si 1 Kg de T2 cuesta 8 $, entonces 1 gr costaría 1/125 $.
    En este caso, tengo:

    minimizar (1/100) * t1 + (1/125) * t2
    dado que
    3 * t1 + 2 * t2 >= 3
    1 * t1 + 3 * t2 >= 1.5
    8 * t1 + 2 * t2 >= 4
    
    En ambos casos se puedo despejar t2 de las desigualdades:
    t2 >= (1 / 2) * (3 - 3 * t1) [ recta 1 ]
    t2 >= (1 / 3) * (3 / 2 - t1) [ recta 2 ]
    t2 >= 2 - 4 * t1             [ recta 3 ]

    b. Graficar la región factible
    c. La solución se puede encontrar con scipy.optimize
    Para usar optimize.linprog necesitamos que el problema este planteado de la 
    siguiente forma (A_{...} matriz y el resto vectores):
    min c.T x
    A_{ub} <= b_{ub}
    A_{eq} =  b_{eq}
    l <= x <= u (por defecto l = 0, u = None)
    Por ello, tenemos en la segunda forma:
    min [10, 8].T @ x
    [[-3, -2], [-1, -3], [-8, -2]] <= [[-3],[-1.5],[-4]]
    [[1, 1]] = [[1]]

"""
def ej1():
    t1 = np.arange(0, 2, 0.1)
    t2_1 = (1/2) * (3 - 3 * t1)
    t2_2 = (1/3) * (1.5 - t1)
    t2_3 = 2 - 4 * t1

    res = optimize.linprog(
        c = np.array([1/100, 1/125]),
        A_ub = np.array([
            [-3, -2],
            [-1, -3],
            [-8, -2]
        ]),
        b_ub = np.array([-3, -1.5, -4]),
        bounds = [(0, None), (0, None)]
    )
    
    print("Éxito: {}\n".format(res.success))
    print("Iteraciones: {}\n".format(res.nit))
    print(res.message + "\n")
    if res.success:
        print("Solución:")
        print(res.x)
        print("\n")
        print("Valor de la función objetivo: {}\n".format(res.fun))
        pyplot.plot(res.x[0], res.x[1], "ro", label = "Solución: ({},{})".format(res.x[0], res.x[1]))

    tmax = np.maximum(np.maximum(t2_1, t2_2), t2_3)
    pyplot.plot(t1, t2_1, label = "$t_{2} = (1/2)(3 - 3 t_{1})$")
    pyplot.plot(t1, t2_2, label = "$t_{2} = (1/3)(1.5 - t_{1})$")
    pyplot.plot(t1, t2_3, label = "$t_{2} = 2 - 4 t_{1}$")
    pyplot.legend(loc="upper right")
    pyplot.axhline(0, color='black')
    pyplot.axvline(0, color='black')
    pyplot.ylim(0, 3)
    pyplot.xlim(0, 1)
    pyplot.ylabel("$t_{2}$")
    pyplot.xlabel("$t_{1}$")
    pyplot.fill_between(t1, tmax, 3 , alpha = 0.5)

    pyplot.grid()
    pyplot.show()

""" Ejercicio 2 
    El problema a resolver y graficar sería:
    
    maximizar x + y
    dado que
    50 * x + 24 * y <= 2400
    30 * x + 33 * y <= 2100
    
    Equivale a:
    
    minimizar - x - y
    50 * x + 24 * y <= 2400
    30 * x + 33 * y <= 2100

    Tenemos que:
    y <= (1/24) * (2400 - 50 * x)
    y <= (1/33) * (2100 - 30 * x)
    Para graficar:
    y = (1/24) * (2400 - 50 * x)
    y = (1/33) * (2100 - 30 * x)
    Podemos usar las siguientes rectas para entender donde se debe llenar la región:
    y = (1/24) * (2300 - 50 * x)
    y = (1/33) * (2000 - 30 * x)
"""
def ej2():
    x = np.arange(0, 50, 1.)
    y1 = (1/24) * (2400 - 50 * x)
    y2 = (1/33) * (2100 - 30 * x)

    # Orientadores
    #y1_1 = (1/24) * (2300 - 50 * x)
    #y2_1 = (1/33) * (2000 - 30 * x)

    res = optimize.linprog(
        c = np.array([-1, -1]),
        A_ub = np.array([
            [50, 24],
            [30, 33]
        ]),
        b_ub = np.array([2400, 2100]),
        bounds = [(0, None), (0, None)]
    )
    
    print("Éxito: {}\n".format(res.success))
    print("Iteraciones: {}\n".format(res.nit))
    print(res.message + "\n")
    if res.success:
        print("Solución:")
        print(res.x)
        print("\n")
        print("Valor de la función objetivo: {}\n".format(res.fun))
        pyplot.plot(res.x[0], res.x[1], "ro", label = "Solución: ({},{})".format(res.x[0], res.x[1]))
    
    ymin = np.minimum(y1, y2)
    pyplot.plot(x, y1, label = "$y = (1/24) (2400 - 50 x)$")
    pyplot.plot(x, y2, label = "$y = (1/33) (2100 - 30 x)$")
    #pyplot.plot(x, y1_1)
    #pyplot.plot(x, y2_1)
    pyplot.legend(loc="upper right")
    pyplot.axhline(0, color='black')
    pyplot.axvline(0, color='black')
    pyplot.ylim(0, 50)
    pyplot.xlim(0, 50)
    pyplot.ylabel("$y$")
    pyplot.xlabel("$x$")
    pyplot.fill_between(x, 0, ymin, alpha = 0.5)

    pyplot.grid()
    pyplot.show()

""" Ejercicio 3
    Podemos tener la tabla hierbas medicinales para cada uno de los medicamentos.
    Por unidad  A  B
    M1          3  2
    M1 cura en 25 unidades de salud

    Por unidad  A  B
    M2          4  1
    M2 cura en 20 unidades de salud

    Disponibilidad de A: 25, o sea 0 <= A <= 25
    Disponibilidad de B: 10, o sea 0 <= B <= 10

    ¿Cuántas unidades de cada medicamento debemos crear para maximizar la curación?
    a. Plantear el problema.
    Quiero maximizar la proporción necesaria de medicamentos: 25 * m1 + 20 * m2
    Siempre m1, m2 >= 0
    Además, lo que se use de a hierbas A y B debe ser suma de las proporciones que
    correspondan:
    A = 3 * m1 + 4 * m2
    B = 2 * m1 + m2
    Entonces queda:
    minimizar -25 * m1 - 20 * m2
    dado que
    3 * m1 + 4 * m2 <= 25
    2 * m1 + m2     <= 10

    b. Graficar.
    Uso las rectas:
    m2 = (1/4) * (25 - 3 * m1) [ recta 1 ]
    m2 = 10 - 2 * m1           [ recta 2 ]

    Para orientar uso las rectas:
    m2 = (1/4) * (20 - 3 * m1) [ recta 1 ]
    m2 = 11 - 2 * m1           [ recta 2 ]
    c. Resolver.
"""
def ej3():
    m1 = np.arange(0, 10, 0.1)
    m2_1 = (1/4) * (25 - 3 * m1)
    m2_2 = 10 - 2 * m1
    
    # Orientadores
    #m2_1_1 = (1/4) * (20 - 3 * m1)
    #m2_2_1 = 11 - 2 * m1

    res = optimize.linprog(
        c = np.array([-25, -20]),
        A_ub = np.array([
            [3, 4],
            [2, 1]
        ]),
        b_ub = np.array([25, 10]),
        bounds = [(0, None), (0, None)]
    )
    
    print("Éxito: {}\n".format(res.success))
    print("Iteraciones: {}\n".format(res.nit))
    print(res.message + "\n")
    if res.success:
        print("Solución:")
        print(res.x)
        print("\n")
        print("Valor de la función objetivo: {}\n".format(res.fun))
        pyplot.plot(res.x[0], res.x[1], "ro", label = "Solución: ({},{})".format(res.x[0], res.x[1]))

    pyplot.plot(m1, m2_1, label = "$m_{2} = (1/24) (2400 - 50 m_{1})$")
    pyplot.plot(m1, m2_2, label = "$m_{2} = (1/33) (2100 - 30 m_{1})$")
    #pyplot.plot(m1, m2_1_1)
    #pyplot.plot(m1, m2_2_1)
    pyplot.legend(loc="upper right")
    pyplot.axhline(0, color='black')
    pyplot.axvline(0, color='black')
    pyplot.ylim(0, 15)
    pyplot.xlim(0, 10)
    pyplot.ylabel("$m_{2}$")
    pyplot.xlabel("$m_{1}$")
    pyplot.fill_between(m1, m2_1, m2_2, where = m2_1 > m2_2, alpha = 0.5)

    pyplot.grid()
    pyplot.show()

""" Ejercicio 4
    ¿Cuál es la cantidad a fabricar de cada tipo de cerveza, de manera que las ventas
    sea máxima?
    Busco maximizar las ventas, ie, maximizar 7 * rubia + 4 * negra + 3 * baja
    de forma que respete la disponibilidad de cada recurso.
    Según la tabla:
    Malta    = rubia + 2 * negra + 2 * baja <= 30
    Levadura = 2 * rubia + negra + 2 * baja <= 45
    Entonces tengo el problema:
    
    minimizar -7 * rubia - 4 * negra - 3 * baja
    dado que
    rubia + 2 * negra + 2 * baja <= 30
    2 * rubia + negra + 2 * baja <= 45
    rubia, negra, baja >= 0

    Si quiero graficar esto, veo que tengo los hiperplanos:
    rubia + 2 * negra + 2 * baja = 30
    2 * rubia + negra + 2 * baja = 45
    Despejo rubia:
    rubia = 30 - 2 * negra - 2 * baja
    rubia = (1/2) * (45 - negra - 2 * baja)
    Y para orientar uso:
    rubia = 20 - 2 * negra - 2 * baja
    rubia = (1/2) * (35 - negra - 2 * baja)

"""
def ej4():
    res = optimize.linprog(
        c = np.array([-7, -4, -3]),
        A_ub = np.array([
            [1, 2, 2],
            [2, 1, 2]
        ]),
        b_ub = np.array([30, 45]),
        bounds = [(0, None), (0, None), (0, None)]
    )

    print("Éxito: {}\n".format(res.success))
    print("Iteraciones: {}\n".format(res.nit))
    print(res.message + "\n")
    if res.success:
        print("Solución:")
        print(res.x)
        print("\n")
        print("Valor de la función objetivo: {}\n".format(res.fun))

""" Ejercicio 5 """
def ej5():
    return None

""" Ejercicio 6 """
def ej6():
    return None
