# Ejercicio 1


def fibonacci(n):
    """ Devuelve una lista con los primeros n números de Fibonacci
        según la definición del pdf
    """
    if isinstance(n, int):
        if n > 0:
            if n == 1:
                return [0]
            elif n == 2:
                return [0, 1]
            else:
                i = 3
                """ Observación: fib[i-1] guarda el i-ésimo número de Fibonacci """
                fib = [0, 1]
                """ Este loop es correcto: para obtener el n-ésimo número 
                    de Fibonacci, este pasa a ocupar el (n-1)-ésimo lugar en fib
                    con lo que debemos usar los dos anteriores en fib
                """
                while i <= n:
                    fib.append(fib[i - 2] + fib[i - 3])
                    i += 1
                return fib
        else:
            print("ERROR: n no es positivo!\n")
            return None
    else:
        print("ERROR: n no es entero!\n")
        return None
