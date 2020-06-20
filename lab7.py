from importlib    import reload
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
    dado que:
    50 * x + 24 * y <= 2400
    30 * x + 33 * y <= 2100
    
    Equivale a:
    
    minimizar - x - y
    dado que:
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
    dado que:
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
        print("Proporción M1: {}\n".format(res.x[0]))
        print("Proporción M2: {}\n".format(res.x[1]))
        print("\n")
        print("Valor de la función objetivo: {}\n".format(-res.fun))
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
    dado que:
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
        print("Venta de Rubia: {}\n".format(res.x[0]))
        print("Venta de Negra: {}\n".format(res.x[1]))
        print("Venta de Baja: {}\n".format(res.x[2]))
        print("\n")
        print("Valor de la función objetivo: {}\n".format(-res.fun))

""" Ejercicio 5
    Se quiere saber el número de horas de trabajo que deben asignarse a cada equipo
    para que se minimice el coste total del montaje del sistema.
    Sean x1, x2, x3, x4 las horas totales de trabajo asignadas a los equipos 1, 2, 3, 4,
    respectivamente.
    El problema consitría en minimizar :
    68.3 * x1 + 69.5 * x2 + 71 * x3 + 71.2 * x4
    Según la tabla tendriamos que:
    x1 <= 220
    x2 <= 300
    x3 <= 245
    x4 <= 190
    Las tareas completas lleva en horas:
    Equipo  M    N    P    Q
    1       52   212  25   60
    2       57   218  23   57
    3       51   201  26   54
    4       56   223  21   55
    Si vemos desde la perspectiva de los equipos, tendríamos que ver 
    cuanto de cada tarea le lleva a los equipos. Entonces introducimos las variables 
    {m1, ..., m4}, ..., {q1, ..., q4}, que nos dan las horas que cada equipo dan a
    las tareas M, N, P, Q. Entonces:
    x1 = m1 + n1 + p1 + q1 <= 220
    x2 = m2 + n2 + p2 + q2 <= 300
    x3 = m3 + n3 + p3 + q3 <= 245
    x4 = m4 + n4 + p4 + q4 <= 190
    Y la función objetivo es:
    68.3 * (m1 + n1 + p1 + q1) + 69.5 * (m2 + n2 + p2 + q2) + 
    71   * (m3 + n3 + p3 + q3) + 71.2 * (m4 + n4 + p4 + q4)
    Ahora bien, cada tarea debe completarse, con lo que la proporción
    (Horas dedicadas a la tarea por el equipo i) / (Horas que lleva completar al equipo i)
    i = 1, ..., 4. Entonces:
    m1 * (1 / 52 ) + m2 * (1 / 57 ) + m3 * (1 / 51 ) + m4 * (1 / 56 ) >= 1
    n1 * (1 / 212) + n2 * (1 / 218) + n3 * (1 / 201) + n4 * (1 / 223) >= 1
    p1 * (1 / 25 ) + p2 * (1 / 23 ) + p3 * (1 / 26 ) + p4 * (1 / 21 ) >= 1
    q1 * (1 / 60 ) + q2 * (1 / 57 ) + q3 * (1 / 54 ) + q4 * (1 / 55 ) >= 1
    Para usar scipy.optimize.linprog:
    m1 * (-1 / 52 ) + m2 * (-1 / 57 ) + m3 * (-1 / 51 ) + m4 * (-1 / 56 ) <= -1
    n1 * (-1 / 212) + n2 * (-1 / 218) + n3 * (-1 / 201) + n4 * (-1 / 223) <= -1
    p1 * (-1 / 25 ) + p2 * (-1 / 23 ) + p3 * (-1 / 26 ) + p4 * (-1 / 21 ) <= -1
    q1 * (-1 / 60 ) + q2 * (-1 / 57 ) + q3 * (-1 / 54 ) + q4 * (-1 / 55 ) <= -1

    Nos queda el problema:
    Minimizar
    68.3 * m1 + 68.3 * n1 + 68.3 * p1 + 68.3 * q1 + 
    69.5 * m2 + 69.5 * n2 + 69.5 * p2 + 69.5 * q2 + 
    71   * m3 + 71   * n3 + 71   * p3 + 71   * q3 + 
    71.2 * m4 + 71.2 * n4 + 71.2 * p4 + 71.2 * q4
    
    Dado que:
    m1 * (-1 / 52 ) + n1 * 0 + p1 * 0 + q1 * 0 +
    m2 * (-1 / 57 ) + n2 * 0 + p2 * 0 + q2 * 0 +
    m3 * (-1 / 51 ) + n3 * 0 + p3 * 0 + q3 * 0 +
    m4 * (-1 / 56 ) + n4 * 0 + p4 * 0 + q4 * 0
    <= -1
    
    m1 * 0 + n1 * (-1 / 212) + p1 * 0 + q1 * 0 +
    m2 * 0 + n2 * (-1 / 218) + p2 * 0 + q2 * 0 +
    m3 * 0 + n3 * (-1 / 201) + p3 * 0 + q3 * 0 +
    m4 * 0 + n4 * (-1 / 223) + p4 * 0 + q4 * 0
    <= -1
    
    m1 * 0 + n1 * 0 + p1 * (-1 / 25 ) + q1 * 0 + 
    m2 * 0 + n2 * 0 + p2 * (-1 / 23 ) + q2 * 0 + 
    m3 * 0 + n3 * 0 + p3 * (-1 / 26 ) + q3 * 0 + 
    m4 * 0 + n4 * 0 + p4 * (-1 / 21 ) + q4 * 0 
    <= -1
    
    m1 * 0 + n1 * 0 + p1 * 0 + q1 * (-1 / 60 ) +
    m2 * 0 + n2 * 0 + p2 * 0 + q2 * (-1 / 57 ) +
    m3 * 0 + n3 * 0 + p3 * 0 + q3 * (-1 / 54 ) +
    m4 * 0 + n4 * 0 + p4 * 0 + q4 * (-1 / 55 )
    <= -1
    
    m1 * 1 + n1 * 1 + p1 * 1 + q1 * 1 +
    m2 * 0 + n2 * 0 + p2 * 0 + q2 * 0 +
    m3 * 0 + n3 * 0 + p3 * 0 + q3 * 0 +
    m4 * 0 + n4 * 0 + p4 * 0 + q4 * 0
    <= 220

    m1 * 0 + n1 * 0 + p1 * 0 + q1 * 0 +
    m2 * 1 + n2 * 1 + p2 * 1 + q2 * 1 + 
    m3 * 0 + n3 * 0 + p3 * 0 + q3 * 0 +
    m4 * 0 + n4 * 0 + p4 * 0 + q4 * 0
    <= 300
    
    m1 * 0 + n1 * 0 + p1 * 0 + q1 * 0 +
    m2 * 0 + n2 * 0 + p2 * 0 + q2 * 0 +
    m3 * 1 + n3 * 1 + p3 * 1 + q3 * 1 +
    m4 * 0 + n4 * 0 + p4 * 0 + q4 * 0    
    <= 245
    m1 * 0 + n1 * 0 + p1 * 0 + q1 * 0 +
    m2 * 0 + n2 * 0 + p2 * 0 + q2 * 0 +
    m3 * 0 + n3 * 0 + p3 * 0 + q3 * 0 +    
    m4 * 1 + n4 * 1 + p4 * 1 + q4 * 1
    <= 190
    
    m1, ..., m4, n1, ..., n4, p1, ..., p4, q1, ..., q4 => 0
"""
def ej5():
    c = np.concatenate([
        np.repeat(68.3, 4),
        np.repeat(69.5, 4),
        np.repeat(71  , 4),
        np.repeat(71.2, 4)
    ])
    A_ub = np.array([
        [-1/52, 0, 0, 0, -1/57, 0, 0, 0, -1/51, 0, 0, 0, -1/56, 0, 0, 0],
        [0, -1/212, 0, 0, 0, -1/218, 0, 0, 0, -1/201, 0, 0, 0, -1/223, 0, 0],
        [0, 0, -1/25, 0, 0, 0, -1/23, 0, 0, 0, -1/26, 0, 0, 0, -1/21, 0],
        [0, 0, 0, -1/60, 0, 0, 0, -1/57, 0, 0, 0, -1/54, 0, 0, 0, -1/55],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
    ])
    b_ub = np.concatenate([
        np.repeat(-1, 4),
        np.array([220, 300, 245, 190])
    ])
    bounds = [
        (0, None), (0, None), (0, None), (0, None),
        (0, None), (0, None), (0, None), (0, None),
        (0, None), (0, None), (0, None), (0, None),
        (0, None), (0, None), (0, None), (0, None)
    ]

    res = optimize.linprog(
        c = c,
        A_ub = A_ub,
        b_ub = b_ub,
        bounds = bounds,
        method = "interior-point"
    )

    print("Éxito: {}\n".format(res.success))
    print("Iteraciones: {}\n".format(res.nit))
    print(res.message + "\n")
    if res.success:
        print("Solución:")
        for i in range(4):
            print("Horas Equipo {}: {}".format(i + 1,
                round(res.x[4 * i] + res.x[4 * i + 1] + res.x[4 * i + 2] + res.x[4 * i + 3])
            ))
            print("M: {}, N: {}, P: {}, Q: {}\n".format(round(res.x[4 * i]), round(res.x[4 * i + 1]), round(res.x[4 * i + 2]), round(res.x[4 * i + 3])))
        print("\n")
        print("Valor de la función objetivo: {}\n".format(res.fun))

""" Ejercicio 6
    Una empresa cosechadora y proveedora de maní debe llevar su producción (almacenada
    en 100 molinos) a sus clientes (100 locales diferentes).
    Los datos que tenemos:
    costos.dat  -> La entrada (i, j) representa el costo de enviar la prodcucción desde
                   el depósito i al cliente j. Debe tener dimensión (100, 100).
    stock       -> La entrada i tiene el stock del depósito i. Tiene dimensión (100,).
    demanda.dat -> La entrada j tiene la demanda del cliente j. Tiene dimensión (100,).
    Se desea minimizar el costo de transportar el producto de los depósitos a los 
    clientes, sujeto al stock. Tenemos el siguiente problema:
    
    minimizar Suma(i, j) Costo[i, j] @ x[i, j]
    dado que:
     Suma(j) x[i, j] <=  Stock[i]
    -Suma(i) x[i, j] <= -Demanda[j]
    x[i, j] >= 0

    Tenemos, por lo tanto, 100 * 100 = 10000 variables (los x aquí).
    La función de costo sería de la forma (poniendo todas las filas pegadas):
    Suma(j) Costo[1, j] * x[1, j] +
    Suma(j) Costo[2, j] * x[2, j] +
    ...
    Suma(j) Costo[100, j] * x[100, j]

    La suma sobre los stocks se hace por fila.
    Suma(j) x[1, j]   <= Stock[1]   -> 1 ... 1 | 0 ... 0 | ... | 0 ... 0
    Suma(j) x[2, j]   <= Stock[2]   -> 0 ... 0 | 1 ... 1 | ... | 0 ... 0
    ...
    Suma(j) x[100, j] <= Stock[100] -> 0 ... 0 | 0 ... 0 | ... | 1 ... 1
    La suma por la demanda se hace por las columnas.
    -Suma(i) x[i, 1]   <= -Demanda[1]   -> -1  0 ...  0 | -1  0 ...  0 | ... | -1  0 ...  0
    -Suma(i) x[i, 2]   <= -Demanda[2]   ->  0 -1 ...  0 |  0 -1 ...  0 | ... |  0 -1 ...  0
    ...
    -Suma(i) x[i, 100] <= -Demanda[100] ->  0  0 ... -1 |  0  0 ... -1 | ... |  0  0 ... -1
    Tenemos un vector de restricciones de 200 elementos.
    
"""
def ej6():
    Costos  = np.loadtxt("./Datos_Laboratorio_7/costos.dat", dtype = "float")
    Stock   = np.loadtxt("./Datos_Laboratorio_7/stock.dat", dtype = "float")
    Demanda = np.loadtxt("./Datos_Laboratorio_7/demanda.dat", dtype = "float")
    # Dimensión (10000,)
    c = Costos.flatten()
    # Dimensión (200,)
    b_ub = np.hstack((Stock, -Demanda))
    # Dimensión (200, 10000)
    A_ub = np.vstack(
        ( np.kron(np.eye(100), np.ones(100)), np.kron(np.ones(100), -np.eye(100)) )
    )
    # Dimensión (10000,)
    bounds = 10000 * [(0, None)]

    res = optimize.linprog(
        c = c,
        A_ub = A_ub,
        b_ub = b_ub,
        bounds = bounds,
        method = "interior-point"
    )

    print("Éxito: {}\n".format(res.success))
    print("Iteraciones: {}\n".format(res.nit))
    print(res.message + "\n")
    if res.success:
        print("Solución:\n")
        for i in range(100):
            for j in range(100):
                if round(res.x[100 * i + j]) > 0:
                    print("Del depósito {} se transporta al cliente {} aprox. {} unidades".format(
                        i + 1,
                        j + 1,
                        round(res.x[100 * i + j])
                    ))
        print("\n")
        print("Valor de la función objetivo: {}\n".format(res.fun))
