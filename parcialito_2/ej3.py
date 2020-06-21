# Ejercicio 3
from matplotlib     import pyplot
from scipy.optimize import linprog
import numpy as np

""" Ejercicio 3
    El cliente solo fabrica mesas y sillas, y vende toda su fabricación en un mercado.
    Sea M, S, TP, MP las abreviaturas para "Mesa", "Silla", "Tiempo de producción" y 
    "Materia prima", respectivamente.
    De la consigna sacamos los siguientes datos en limpio:
    por unidad        | TP   | MP   | 
    M                 | 2  h | 1  p | 
    S                 | 1  h | 2  p | 
    Disponible/semana | 40 h | 50 p |
    * donde h sería hora/s y p sería plancha/planchas.
    
"""

""" Ejercicio 3.a
    ¿Cuántas mesas y sillas debe fabricar por semana para maximizar sus ingresos?
    Indicar el ingreso máximo.

    por unidad        | TP   | MP   | Ingreso | 
    M                 | 2  h | 1  p | 500 $   |
    S                 | 1  h | 2  p | 300 $   |
    Disponible/semana | 40 h | 50 p |
    * aquí el símbolo $ se refiere a pesos.
    
    Sea m y s las mesas y sillas que se pueden vender en el periodo de una semana.
    Se busca maximizar 500 * m + 300 * s, y las restricciones:
    2 * m + 1 * s <= 40
    1 * m + 2 * s <= 50
    m, s >= 0

    O sea, debemos resolver:
    minimizar -500 * m - 300 * s
    sujeto a:
    2 * m + 1 * s <= 40
    1 * m + 2 * s <= 50
    m, s >= 0

    Rectas para graficar:
    2 * m + s = 40 -> s = -2 * m + 40       [ recta 1 ]
    m + 2 * s = 50 -> s = (1/2) * (-m + 50) [ recta 2 ]
    Para orientar usamos:
    s = -2 * m + 30
    s = (1/2) * (-m + 40)

    [nota]
    En realidad voy a usar round para el vector solución y calcular el valor de la
    función objetivo de acuerdo a lo obtenido. 
"""
def ej3_a():
    """ Da la respuesta del ejercicio 3.a """
    c = np.array([-500, -300])
    A_ub = np.array([
        [2, 1],
        [1, 2]
    ])
    b_ub = np.array([40, 50])
    bounds = [(0, None), (0, None)]
    
    res = linprog(
        c = c,
        A_ub = A_ub,
        b_ub = b_ub,
        bounds = bounds,
        method = "interior-point"
    )

    print("Éxito: {}\n".format(res.success))
    print("Iteraciones: {}\n".format(res.nit))
    print("Status: {}\n".format(res.status))
    print(res.message + "\n")
    if res.success:
        print("Nuestro cliente necesita fabricar al menos:\n")
        print("Mesas: {} unidades\n".format(round(res.x[0])))
        print("Sillas: {} unidades\n".format(round(res.x[1])))
        print("Ingreso neto maximizado con los recursos disponibles: {}\n".format(
                500 * round(res.x[0]) + 300 * round(res.x[1])
        ))

""" Ejercicio 3.b
    Dibujar la región factible del problema.
"""
def ej3_b():
    """ Da la respuesta del ejercicio 3.b """
    m = np.linspace(0, 20, 100)
    s_1 = -2 * m + 40
    s_2 = (1/2) * (-m + 50)
    
    # Orientadores
    #s_1_o = -2 * m + 30
    #s_2_o = (1/2) * (-m + 40)
    
    pyplot.plot(m, s_1,   label = "$s = -2 m + 40$")
    pyplot.plot(m, s_2,   label = "$s = (1/2) * (-m + 50)$")
    #pyplot.plot(m, s_1_o)
    #pyplot.plot(m, s_2_o)
    pyplot.legend(loc = "upper right")
    pyplot.axhline(0, color = "black")
    pyplot.axvline(0, color = "black")
    pyplot.ylim(0, 40)
    pyplot.xlim(0, 20)
    pyplot.ylabel("$s$")
    pyplot.xlabel("$m$")
    pyplot.fill_between(m, 0, np.minimum(s_1, s_2), alpha = 0.75)

    pyplot.grid()
    pyplot.show()

""" Ejercicio 3.c
    Supongamos que el cliente contrata a un ayudante a un costo de 200 $/h,
    ¿Le conviene? En caso afirmativo ¿Por cuántas horas?
    
    Ahora tenemos que ver que las 40 horas disponibles y las 50 planchas disponibles
    se reparten entre dos trabajadores.
    Entonces sean:
    mc: Producción de mesas del cliente.
    ma: Producción de mesas del ayudante.
    sc: Producción de sillas del cliente.
    sa: Producción de sillas del ayudante.
    
    El problema es:

    minimizar -500 * mc - 500 * ma - 300 * sc - 300 * sa
    sujeto a.:
    2 * mc + 2 * ma + 1 * sc + 1 * sa <= 40
    1 * mc + 1 * ma + 2 * sc + 2 * sa <= 50
    mc, ma, sc, sa >= 0

    Supongamos que obtenemos como respuesta la tupla (mc, ma, sc, sa) y el valor
    de la función objetivo es V (que sería -res.fun usando linprog), entonces el 
    cliente debe pagar a su ayudante:

    Horas trabajadas por el ayudante = 2 * ma + sa
    Pago del ayudante = 200 * Horas trabajadas por el ayudante
                      = 200 * (2 * ma + sa)
    Ingreso del cliente = V - Pago del ayudante

    [nota] 
    En realidad voy a usar round para el vector solución y calcular el valor de la
    función objetivo de acuerdo a lo obtenido. 
"""
def ej3_c():
    """ Da la respuesta del ejercicio 3.c """
    c = np.array([-500, -500, -300, -300])
    A_ub = np.array([
        [2, 2, 1, 1],
        [1, 1, 2, 2]
    ])
    b_ub = np.array([40, 50])
    bounds = [(0, None), (0, None), (0, None), (0, None)]
    
    res = linprog(
        c = c,
        A_ub = A_ub,
        b_ub = b_ub,
        bounds = bounds,
        method = "interior-point"
    )
    
    print("Éxito: {}\n".format(res.success))
    print("Iteraciones: {}\n".format(res.nit))
    print("Status: {}\n".format(res.status))
    print(res.message + "\n")
    if res.success:
        """ mc: res.x[0]
            ma: res.x[1]
            sc: res.x[2]
            sa: res.x[3]
        """
        horas_ayudante = 2 * round(res.x[1]) + round(res.x[3]) 
        neto = 500 * round(res.x[0]) + 500 * round(res.x[1]) +\
               300 * round(res.x[2]) + 300 * round(res.x[3])
        paga_ayudante = 200 * horas_ayudante
        porcentaje_ingreso = round(100 - 100 * (paga_ayudante / neto))
        print("Ingreso neto por el trabajo: {}\n".format(neto))
        print("Paga correspondiente al ayudante: {}\n".format(paga_ayudante))
        print("Ingreso del cliente: {}\n".format(neto - paga_ayudante))
        print("Porcentaje de ingreso del cliente ~ {} %\n".format(porcentaje_ingreso))
        if 75 <= porcentaje_ingreso:
            print("El ingreso del cliente es mayor o igual al 75%, y quizás da un buen margen para renovar el depósito.")
            print("En este caso el ayudante trabajaría {} h más o menos.\n".format(horas_ayudante))
        elif 60 <= porcentaje_ingreso < 75:
            print("El ingreso del cliente es mayor o igual al 60% pero no supera el 75%, y quizás da un cierto margen para renovar el depósito.")
            print("En este caso el ayudante trabajaría {} h más o menos.\n".format(horas_ayudante))
        elif 50 <= porcentaje_ingreso < 60:
            print("El ingreso del cliente es mayor o igual al 50% pero no supera el 60%, y quizás no da un buen margen para renovar el depósito.")
            print("En este caso el ayudante trabajaría {} h más o menos.\n".format(horas_ayudante))
        else:
            print("El ingreso del cliente es menor al 50% y quizás haya que estudiar mejor la contratación.\n")
