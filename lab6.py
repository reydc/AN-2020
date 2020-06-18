from importlib  import reload
import numpy as np
import scipy.linalg as splinalg

""" Ejercicio 1 """

""" Resolver el sistema triangular superior """
def soltrsup(A, b):
    """ A es una matriz triangular superior R^(n*n)
        b es un vector de R^n
        retorna la solución x (en R^n)
    """
    n = A.shape[0]
    x = b.copy()
    for i in range(n - 1, -1 , -1):
        for j in range(i + 1, n):
            x[i] = x[i] - A[i, j] * x[j]
        x[i] = x[i] / A[i, i]
    return x

""" Resolver el sistema triangular inferior """
def soltrinf(A, b):
    """ A es una matriz triangular inferior R^(n*n)
        b es un vector de R^n
        retorna la solución x (en R^n)
    """
    n = A.shape[0]
    x = b.copy()
    for i in range(0, n):
        for j in range(0, i):
            x[i] = x[i] - A[i, j] * x[j]
        x[i] = x[i] / A[i, i]
    return x

""" Ejemplo 1 (triangular superior) """
A1 = np.array([
    [1., 2., 3.],
    [0., 4., 5.],
    [0., 0., 6.]
])
b1 = np.array([
    [10.], 
    [13.],
    [6.]
])

""" Ejemplo 2 (triangular inferior) """
A2 = np.array([
    [1., 0., 0.],
    [0., 2., 0.],
    [-1., 5., -3.]
])
b2 = np.array([
    [2.],
    [8.],
    [0.]
])

""" Ejemplo 3 (triangular superior) """
A3 = np.array([
    [2, -1, 1, 0, 3],
    [0, 4, 5,10, 2],
    [0, 0, -5, 0, 11],
    [0, 0, 0, 2, -7],
    [0, 0, 0, 0, 40]
])
b3 = np.array([
    [5.],
    [21.],
    [6.],
    [-5.],
    [40.]
])

def ej1_ejemplo():
    """ Práctico 6 del 2020, ejercicio 1 """
    x1 = soltrsup(A1, b1)
    x2 = soltrinf(A2, b2)
    x3 = soltrsup(A3, b3)
    print("A1 * x1 = b1\n")
    print(x1)
    print("\n")
    print("A2 * x2 = b2\n")
    print(x2)
    print("\n")
    print("A3 * x3 = b3\n")
    print(x3)
    print("\n")

""" Ejercicio 2 """

def egauss(A, b):
    """ A es una matriz R^(n*n)
        b es un vector de R^n
        retorna el par (U, y), donde
        U es una matriz triangular R^(n*n)
        y es un vector de R^n, la solución
    """
    n = A.shape[0]
    U = A.copy()
    y = b.copy()
    for k in range(n - 1):
        for i in range(k + 1, n):
            if U[k,k] == 0:
                print("[ egauss ] No se puede seguir la eliminación gaussiana: U[{}, {}] == 0\n".format(k, k))
                raise ValueError("U[{}, {}] == 0\n".format(k, k))
            m = U[i, k] / U[k, k]
            for j in range(k + 1, n):
                U[i, j] = U[i, j] - m * U[k, j]
            y[i] = y[i] - m * y[k]
    U = np.triu(U)
    return U, y

def soleg(A, b):
    """ A es una matriz R^(n*n)
        b es un vector de R^n
        retorna la solución x (en R^n)
    """
    try:
        U, y = egauss(A, b)
        x = soltrsup(U, y)
        return x
    except ValueError as e:
        print("[ soleg ] No se pudo realizar la eliminación gaussiana...\n")
        print(e)
        return None

""" Ejercicio 3 """
def sollu(A, b):
    P, L, U = splinalg.lu(A)
    """ Encuentra A = P * L * U, de donde
        A * x = P * L * U * x = b
        Entonces P^(-1) * A * x = L * U * x = P^(-1) * b
        Pero P^(-1) = P^T (la inversa de una matriz de permutación es su traspuesta),
        entonces queda L * U * x = P^T * b, y nos queda resolver
        L * y = P^T * b
        U * x = y
    """
    y = soltrinf(L, P.T @ b)
    x = soltrsup(U, y)
    return x

""" Ejercicio 4 """

D1 = -np.eye(3)
A4 = np.zeros((3, 3), dtype = "float")
np.fill_diagonal(A4, 4)

A4 = np.diagflat(np.full((1,2), -1),-1) + np.diagflat(np.full((1,2), -1), 1) + A4

A_ej4 = np.block([[A4, D1], [D1, A4]])

b1 = np.array([1,1,1,0,0,0], dtype = "float")
b2 = np.array([1,1,1,1,1,1], dtype = "float")

def ej4():
    x1_eg = soleg(A_ej4, b1)
    x1_lu = sollu(A_ej4, b1)

    x2_eg = soleg(A_ej4, b2)
    x2_lu = sollu(A_ej4, b2)

    print("Soluciones b1:\n")
    print("x1_eg:\n")
    print(x1_eg)
    print("x1_lu:\n")
    print(x1_lu)
    print("\nCercanos: ")
    print(np.allclose(A_ej4 @ x1_eg, b1))
    print(np.allclose(A_ej4 @ x1_lu, b1))
    print("\n")
    print("Soluciones b2:\n")
    print("x2_eg:\n")
    print(x2_eg)
    print("x2_lu:\n")
    print(x2_lu)
    print("\nCercanos: ")
    print(np.allclose(A_ej4 @ x2_eg, b2))
    print(np.allclose(A_ej4 @ x2_lu, b2))

""" Ejercicio 5 """
def jacobi(A, b, err, mit):
    """ A es una matriz R^(n*n)
        b es un vector de R^n
        err es la tolerancia de error
        mit es la máxima cantidad de iteraciones
        retorna [x, k], donde
        x es la solución del sistema (en R^n)
        k es la cantidad de iteraciones que se hicieron
    """
    n = A.shape[0]
    k = 0
    x = np.zeros((n, 1))
    while k < mit:
        x_it = np.zeros((n, 1))
        for i in range(n):
            s = 0
            for j in range(i):
                s = s + A[i, j] * x[j]
            for j in range(i+1, n):
                s = s + A[i, j] * x[j]
            x_it[i] = (b[i] - s) / A[i, i]
        """ Ver si se acerca o no """
        norm = np.linalg.norm(x_it - x, np.inf)
        if norm <= err:
            print("[ jacobi ] || x_it - x ||(inf) == {} <= {}\n".format(norm, err))
            return [x_it, k]
        """ No se acerca, sigo iterando """
        x = x_it
        k += 1
    
    return [x, k]

def gseidel(A, b, err, mit):
    """ A es una matriz R^(n*n)
        b es un vector de R^n
        err es la tolerancia de error
        mit es la máxima cantidad de iteraciones
        retorna [x, k], donde
        x es la solución del sistema (en R^n)
        k es la cantidad de iteraciones que se hicieron
    """
    n = A.shape[0]
    k = 0
    x   = np.zeros((n, 1))
    while k < mit:
        x_it = np.zeros((n, 1))
        for i in range(n):
            s = 0
            for j in range(i):
                s = s + A[i, j] * x_it[j]
            for j in range(i+1, n):
                s = s + A[i, j] * x[j]
            
            x_it[i] = (b[i] - s) / A[i, i]
        
        """ Ver si se acerca o no """
        norm = np.linalg.norm(x_it - x, np.inf)
        if norm <= err:
            print("[ gseidel ] || x_it - x ||(inf) == {} <= {}\n".format(norm, err))
            return [x_it, k]
        """ No se acerca, sigo iterando """
        x = x_it
        k += 1
    
    return [x, k]

""" Ejercicio 6 """

A1_ej6 = np.array([
    [3., 1., 1.],
    [2., 6., 1.],
    [1., 1., 4.]
])

b1_ej6 = np.array([
    [5.],
    [9.],
    [6.]
])

A2_ej6 = np.array([
    [5., 7., 6., 5.],
    [7., 10., 8., 7.],
    [6., 8., 10., 9.],
    [5., 7., 9., 10.]
])

b2_ej6 = np.array([
    [23.],
    [32.],
    [33.],
    [31.]
])

""" Probar con ej6_1(100, 100) """
def ej6_1(mit_jacobi, mit_gseidel):
    err = 1e-11
    
    x_jacobi, k_jacobi = jacobi(A1_ej6, b1_ej6, err, mit_jacobi)
    print("Iteración de Jacobi (mit_jacobi = {}):\n".format(mit_jacobi))
    print("iteraciones realizadas: {}\n".format(k_jacobi))
    print(x_jacobi)
    print("\nCercano: {}\n".format(np.allclose(A1_ej6 @ x_jacobi, b1_ej6)))

    x_gseidel, k_gseidel = gseidel(A1_ej6, b1_ej6, err, mit_gseidel)
    print("Iteración de Gauss-Seidel (mit_gseidel = {}):\n".format(mit_gseidel))
    print("iteraciones realizadas: {}\n".format(k_gseidel))
    print(x_gseidel)
    print("\nCercano: {}\n".format(np.allclose(A1_ej6 @ x_gseidel, b1_ej6)))

""" Primero probar con ej6_2(100, 100)
    Después probar con ej6_2(1000, 1000)
"""
def ej6_2(mit_jacobi, mit_gseidel):
    err = 1e-4

    x_jacobi, k_jacobi = jacobi(A2_ej6, b2_ej6, err, mit_jacobi)
    print("Iteración de Jacobi (mit_jacobi = {}):\n".format(mit_jacobi))
    print("iteraciones realizadas: {}\n".format(k_jacobi))
    print(x_jacobi)
    print("\nCercano: {}\n".format(np.allclose(A2_ej6 @ x_jacobi, b2_ej6)))

    x_gseidel, k_gseidel = gseidel(A2_ej6, b2_ej6, err, mit_gseidel)
    print("Iteración de Gauss-Seidel (mit_gseidel = {}):\n".format(mit_gseidel))
    print("iteraciones realizadas: {}\n".format(k_gseidel))
    print(x_gseidel)
    print("\nCercano: {}\n".format(np.allclose(A2_ej6 @ x_gseidel, b2_ej6)))
