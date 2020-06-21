# Ejercicio 2
import numpy as np

""" Para estos ejercicios se debe usar soltrinf para realizar las actualizaciones.
    La salida de las funciones a implementar debe ser [x, k] donde x es la solución
    aproximada y k la cantidad de iteraciones realizadas.
    El algoritmo debe parar si || x_k - x_(k - 1) ||(inf) <= error ó k >= mit.
"""

def soltrinf(A, b):
    """ soltrinf:
        Resuelve el sistema triangular inferior dado por A y b.
        
        Recibe A, b:
        
        A: Es una matriz triangular inferior (R^(n*n)).
        
        b: Es un vector de R^n.
        
        Devuelve x:
        
        x: La solución del sistema (R^n).
    
    """
    n = A.shape[0]
    x = b.copy()
    for i in range(0, n):
        for j in range(0, i):
            x[i] = x[i] - A[i, j] * x[j]
        x[i] = x[i] / A[i, i]
    return x

""" Ejercicio 2.a
    Implementar gseidel.
"""
def gseidel(A, b, err, mit):
    """ gseidel:

        Intenta calcular el vector solución usando el método de iteración de 
        Gauss-Seidel. Se usaría la iteración:

        (L + D) * x(k+1) = b - U * x(k)

        y se despejarían los elementos diagonales.

        Recibe A, b, err, mit:

        A: Matriz del problema (R^(n*n)).

        b: Vector del problema (R^n).

        err: Tolerancia de error.

        mit: Cantidad máxima de iteraciones.

        Devuelve [x, k]:

        x: Posible vector solución (R^n).

        k: Cantidad de iteraciones realizadas.

    """
    n, _ = A.shape
    bb = b.copy()
    if bb.shape == (n,1):
        bb = bb.reshape(n)

    k = 0
    x = np.zeros(n)
    
    A_LD = np.tril(A)
    A_U  = np.triu(A, 1)

    while k < mit:

        x_it = soltrinf(A_LD, bb - (A_U @ x))
        """ Ver si se acerca o no """
        norm = np.linalg.norm(x_it - x, np.inf)
        if norm <= err:
            print("[ gseidel ] || x_it - x ||(inf) == {} <= {}\n".format(norm, err))
            return [x_it, k]
        """ No se acerca, sigo iterando """
        x = x_it
        k += 1
    
    return [x, k]

""" Ejercicio 2.b
    Implementar sor.
"""
def sor(A, b, omega, err, mit):
    """ sor:

        Intenta calcular el vector solución usando el método SOR (Successive
        over-relaxation). Este método consiste en descomponer A como
        A = L + D + U, en la forma usual de los métodos de iteración y usar:

        (D + omega * L) * x(k+1) = omega * b - [omega * U + (omega - 1) * D] * x(k)

        Recibe A, b, omega, err, mit:

        A: Matriz del problema (R^(n*n)).

        b: Vector del problema (R^n).

        omega: Factor de relajación > 1.

        err: Tolerancia de error.

        mit: Cantidad máxima de iteraciones.

        Devuelve [x, k] ó None:

        x: Posible vector solución (R^n).

        k: Cantidad de iteraciones realizadas.

        None: Si omega <= 1.

    """
    if omega <= 1:
        print("[ sor ] omega <= 1. Usar valores omega > 1!\n")
        return None
    
    n, _ = A.shape
    bb = b.copy()
    if bb.shape == (n,1):
        bb = bb.reshape(n)
    
    k = 0
    x = np.zeros(n)

    A_L = np.tril(A, -1)
    A_D = np.diag(np.diag(A))
    A_U = np.triu(A, 1)

    Left  = A_D + omega * A_L
    Right = omega * A_U + (omega - 1) * A_D

    while k < mit:

        x_it = soltrinf(Left , omega * bb - (Right @ x))
        """ Ver si se acerca o no """
        norm = np.linalg.norm(x_it - x, np.inf)
        if norm <= err:
            print("[ sor ] || x_it - x ||(inf) == {} <= {}\n".format(norm, err))
            return [x_it, k]
        """ No se acerca, sigo iterando """
        x = x_it
        k += 1
    
    return [x, k]
