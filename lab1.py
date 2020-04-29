from importlib import reload
from numpy import isinf
from sys   import float_info
from math  import factorial, sqrt

def verificar_propiedades_basicas():
    print("Desde sys.float_info:")
    print("Epsilon = {}".format(float_info.epsilon))
    print("Max Float = {}".format(float_info.max))
    print("Min Float = {}".format(float_info.min))

""" Ejercicio 1 """

def ejercicio_1(x,y,z):
    try:
        print("x/y + z = {}".format(x/y + z))
    except Exception as e:
        print("Excepción para x/y + z")
        print(e)
    try:
        print("x/(y + z) = {}".format(x/(y + z)))
    except Exception as e:
        print("Excepción para x/(y + z)")
        print(e)
    try:
        print("x/y*z = {}".format(x/y*z))
    except Exception as e:
        print("Excepción para x/y*z")
        print(e)
    try:
        print("x/(y*z) = {}".format(x/(y*z)))
    except Exception as e:
        print("Excepción para x/(y*z)")
        print(e)

""" Ejercicio 2 """

def ejercicio_2():
    print("Epsilon-máquina es 2^(-52):")
    print("Recordemos que si eps es el épsilon-máquina, entonces es el número más pequeño tal que 1 + eps != 1")
    print("1 + 2**(-52) = {}".format(1 + 2**(-52)))
    print("1 + 2**(-53) = {}".format(1 + 2**(-53)))

""" Ejercicio 3 """

def ejercicio_3(print_all = True):
    a = 2.
    b = 2.
    if print_all:
        while not isinf(a):
            print("a = {}".format(a))
            a *= 2.
        print("Overflow!")

        while b > 0.:
            print("b = {}".format(b))
            b /= 2.
        print("Underflow!")
    else:
        while not isinf(2. * a):
            a *= 2.
        print("a = {}".format(a))
        print("El próximo causa Overflow!")

        while (b / 2.) > 0.:
            b /= 2.
        print("b = {}".format(b))
        print("El próximo causa Underflow!")

def verificar_ejercicio_3():
    """ Para ver que de lo mismo, con lo que envío el profesor """
    a = 2.
    while a * 2. !=float('inf'):
	    a = a * 2.
    print("a = {}".format(a))
    print("El próximo causa Overflow!")

    b = 2.
    while (b / 2.) != 0.:
	    b /= 2.
    print("b = {}".format(b))
    print("El próximo causa Underflow!")

""" Ejercicio 4 """

def ejercicio_4_a(finite = False, iters = 10):
    """ El comportamiento por defecto es una iteración infinita, usar CTRL+c para detener """
    x = 0
    i = 0
    if finite:
        while i < iters and x != 10.:
            x += 0.1
            i += 1
            print(x)
    else:
        while x != 10.:
            x += 0.1
            print(x)
    
def ejercicio_4_b():
    """ El comportamiento por defecto es una iteración finita """
    x = 0
    while x != 10:
        x += 0.5
        print(x)

""" Ejercicio 5 """

def factorial_rec(n):
    """ Calcula el factorial de n """
    res = 1
    for i in range(2,n+1):
        res *= i
    return res

def ejercicio_5():
    return factorial_rec(6)

def verificar_ejercicio_5(n):
    """ Para chequear que todo anda bien """
    return factorial(n)

""" Ejercicio 6 """
""" Probar con
1)
1.0000000000000003                                                                                                                         
1.0000000000000002
Debe dar "Iguales"
2)
1.0000000000000003
1.0000000000000004
Debe dar "Iguales", pero con tol_rel = 10e-17 debe dar "Distintos"
Después tratar on tol_rel = 0.0, tol_abs = 10e-17
"""
def ejercicio_6(tol_rel = 1e-09, tol_abs = 0.0):
    a = input("Dar un real: ")
    b = input("Dar otro real: ")
    """ Imprimir si son iguales o no
        Usar métodos distintos
    """
    a = float(a)
    b = float(b)
    print("Comparación directa de flotantes:")
    if abs(a - b) > 0:
        print("Distintos")
    else:
        print("Iguales")
    
    """
    tol_abs = Tolerancia absoluta, mientras la diferencia no sea menor se consideran distintos
    tol_rel = Tolerancia relativa, a medida que los valores se vuelven más grandes, se vuelve más
              grande la diferencia permitida mientras que aún se les permitir considerarse iguales
    """
    print("Comparación con tolerancia dada (por defecto: tol_rel = 10e-9, tol_abs = 0.0):")
    if abs(a - b) > max(tol_rel * max(a, b), tol_abs):
        print("Distintos")
    else:
        print("Iguales")

""" Ejercicio 7 """

def potencia(x, n):
    """ x real y n entero 
        casos:
        n >=  0 y x es real
        n < 0 y x != 0 es real
        n < 0 y x == 0 no está definido
    """
    try:
        res = 1.
        if n > 0:
            while n > 0:
                if (n & 1):
                    res = res * x
                x *= x
                n >>= 1
        elif n < 0 and x == 0.:
            raise Exception("n < 0 y x == 0 no está definido...")
        elif n < 0:
            res /= potencia(x, -n) 
        return res
    except Exception as e:
        print(e)

def primeras_5_potencias(x):
    for i in range(1,6):
        print("x**{} = {}".format(i, potencia(x,i)))

""" Ejercicio 8 """
""" Probar con:
    a = 1, b = -10**5, c = 1
    a = 1, b = -40, c = .25    
"""

def buena_alt(a, b, c):
    d = sqrt(b**2 - 4 * a * c)
    x_1 = (-b + d) / (2 * a)
    x_2 = (2 * c) / (-b + d)
    return x_1, x_2

def mala(a, b, c):
    x_1 = (-b + sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    x_2 = (-b - sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    return x_1, x_2

def buena(a, b, c):
    """ Enviada por el profesor """
    """ Vemos cuál b resulta más lejos de 0 """
    if b >= 0:
        x_1 = (-b - sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    else:
        x_1 = (-b + sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    """ Una vez obtenida la primera raíz, recordemos que x_1*x_2 = c/a y usamos eso para obtener x_2 """
    x_2 = c / (a * x_1)
    return x_1, x_2

""" Ejercicio 9 """

def horn(coefs, x):
    a = coefs[len(coefs) - 1]
    for i in range(len(coefs) - 2, -1, -1): 
        a = coefs[i] + x*a
    return a

def horn_alt(coefs, x):
    """ Imprime el polinomio """
    a = coefs[len(coefs) - 1]
    s = (str(a) if a > 0 else "(" + str(a) +")") + \
        ((" * x^" + str(len(coefs) - 1)) if len(coefs) - 1 > 0 else "")
    for i in range(len(coefs) - 2, -1, -1):
        s += (" + "  if coefs[i] >= 0 else " + (") + \
             (str(coefs[i]) if coefs[i] >= 0 else str(coefs[i]) + ")") + \
                 ((" * x^" + str(i)) if i > 0 else "") 
        a = coefs[i] + x*a
    print(s)
    return a