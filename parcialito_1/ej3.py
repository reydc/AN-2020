# Ejercicio 3


""" Inciso a): error_cos estima el error máximo de interpolación para 
               f(x) = cos(x) usando el intervalo especificado por I y
               una cantidad n de puntos interpolantes
"""
def error_cos(I, n):
    if isinstance(n, int) and n > 1:
        if len(I) != 2:
            print("ERROR: I debe estar especificado por dos valores\n")
            return None
        a = I[0]
        b = I[1]
        if b <= a:
            print("ERROR: I debe especificar un intervalo, pero {} <= {}\n".format(b, a))
            return None
        
        """ Tendría n puntos x_i = a + i * h, con i = 0, 1, ..., (n-1)
            Entonces: x_0     == a
                      x_1     == a + 1 * h
                      ...
                      x_(n-1) == a + (n-1) * h == b
            El polinomio interpolante sería de grado <= (n - 1). Luego
            el término de error contemplaría el valor absoluto de la derivada 
            n-ésima, que en caso del coseno está acotada por 1. Además podemos
            acotar el producto de los términos en la fórmula del error según
            el paso h.
            El teorema siguiente se da en "Métodos Numéricos y Computación" 
            de Cheney-Kincaid (sexta edición), Cápitulo 4, sección 2 
            ("Errores de interpolación polinomial"), página 158,
            como el Teorema 2 ("Errores de interpolación II"):

            Sea f una función tal que su derivada (n+1)-ésima es continua
            en [a,b] y sastisface que el valor absoluto de la derivada de 
            ese orden está acotada por M. Sea el p el polinomio de grado
            <= n que interpola a f en n+1 nodos igualmente espaciados en
            [a, b], incluidos los puntos finales. Entonces en [a,b]:
            |f(x) - p(x)| <= M*h**(n+1) / 4*(n+1)
            donde h = (b-a)/n es el espaciamiento entre nodos.

            Este teorema provee una estimación válida, evitando el cálculo del
            factorial en el denominador de la fórmula más directa. Otra estimación 
            se deriva por una desigualdad que se pide probar en el práctico 3 para
            n+1 puntos distantes, incluyendo a los extremos:
            |x-x0|*|x-x1|*...*|x-xn| <= abs(b-a)**(n+1) / 2**(n+1)
            Si lo combinamos con el teorema de error de interpolación que se da
            en el teórico tenemos otra cota:
            M*abs(b-a)**(n+1) / ( (n+1)! * 2**(n+1))
        """
        h = abs(b - a) / (n-1)
        
        return h**n / (4*n)
    else:
        print("ERROR: n no es un entero o bien n <= 1!\n")
        return None


""" Inciso b) """
def inciso_b():
    """ Error pedido """
    error = 1e-6
    
    I = [0, 1]
    n = 2
    
    error_aprox = error_cos(I, n) 
    
    while error_aprox >= error:
        n += 1
        error_aprox = error_cos(I, n)
    
    print("Se necesitan %s puntos para que el error (estimado) sea < %s, error_aprox == %s\n"%(n, error, error_aprox))

    return n
