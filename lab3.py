from importlib  import reload
from matplotlib import pyplot
from numpy      import linspace, loadtxt, isnan
from scipy.interpolate import CubicSpline

""" Ejercicio 1 """
""" Interpolación por la forma de Lagrange """
def ilangrange(x, y, z):
    """ Lista para almacenar los resultados para la lista z """
    resultados = []
    
    if len(x) != len(y):
        print("No están las mismas cantidades de x y f(x)\n\n")
    else:
        """ Multiplicadores de Lagrange evaluados en un punto
            L_i(punto) = Prod(j=0, n, j != i) ( punto - x[j] )/ ( x[i] - x[j] ) 
            resultado[punto] = Suma(i=0, n) y[i] * L_i(punto)
        """
        for k in range(len(z)):
            suma = 0.
            for i in range(len(x)):
                L_i = 1.
                for j in range(len(x)):
                    if j != i:
                        L_i *= (z[k] - x[j])/(x[i] - x[j])
                suma += y[i] * L_i
            resultados.append(suma)
    
    return resultados

""" Ejercicio 2 """
"""  Diferencias divididas, la versión recursiva """
def diferencias_div(x, f, i, j):
    if i == j:
        return f[i]
    elif i < j:
        return ( diferencias_div(x, f, i+1, j) - diferencias_div(x, f, i, j-1) ) / (x[j] - x[i])
    else:
        return 0

def dividida_rec(x,f):
    return [diferencias_div(x, f, 0, j) for j in range(len(x))]

""" Interpolación por la forma Newton, como se pide en el ejercicio 2 """
def inewton_rec(x, y, z):
    """ Lista para almacenar los resultados para la lista z """
    resultados = []

    if len(x) != len(y):
        print("No están las mismas cantidades de x y f(x)\n\n")
    else:
        
        """ Obtenemos los coeficentes, recursivamente """
        c = dividida_rec(x, y)
        
        for k in range(len(z)):
            """ Esquema de Horner
                p(x) = ( ... ( cn * (z[k]) - x(n-1)) + c(n-1) ) * (z[k] - x(n-2) + c(n-2) ) * ... ) *( z[k] - x0) + c0
            """
            suma = c[len(x) - 1]
            for i in range(len(x) - 2, -1, -1):
                suma += suma * (z[k] - x[i]) + c[i] 
            resultados.append(suma)
    
    return resultados

""" Diferencias divididas, sólo la primera fila usando el despeje para la forma de Newton """
def dividida_iter(x, f):
    """ Coeficientes del polinomio en la forma de Newton """
    coefs = []
    """ f[x0, ... , xk] == coefs[k]
        coefs[k] = ( f[k] - 
                    Suma(i=0, k-1) { coefs[i] * Prod(j=0, i-1) ( x[k] - x[j] ) } )
                    / Prod(j=0, k-1) ( x[k] - x[j] )

        En este caso voy a  aprovechar la construcción triangular, pues a medida
        que voy bajando por filas para calcular la siguiente columna, salvo la
        primera fila (que serían los coeficientes), el resto no se necesitan 
    """
    for i in range(len(x)):
        coefs.append(f[i])
    
    for j in range(1, len(x)):
        for i in range(len(x) - 1, j - 1, -1):
            coefs[i] = (coefs[i] - coefs[i - 1]) / (x[i] - x[i - j])
    return coefs

""" Interpolación por la forma Newton, esta vez sólo se usa dividida_iter
    para obtener los coeficientes
"""
def inewton_iter(x, y, z):
    resultados = []
    if len(x) != len(y):
        print("No están las mismas cantidades de x y f(x)\n")
    else:
        """ Obtenemos los coeficientes, iterativamente """
        c = dividida_iter(x, y)
        
        for k in range(len(z)):
            """ Esquema de Horner
                p(x) = ( ... ( cn * (z[k]) - x(n-1)) + c(n-1) ) * (z[k] - x(n-2) + c(n-2) ) * ... ) *( z[k] - x0) + c0
            """
            suma = c[len(x) - 1]
            for i in range(len(x) - 2, -1, -1):
                suma += suma * (z[k] - x[i]) + c[i] 
            resultados.append(suma)
    return resultados

""" Ejercicio 3 """
def ej3():
    """ Puntos para evaluar con nuestro polinomio interpolador """
    z = [24/25 + j/25 for j in range(1, 102)]
    
    f = lambda x : 1/x

    f_z = [f(z_i) for z_i in z]

    """ Queremos interpolar en [1, 2, 3, 4, 5], ie 5 puntos, 
        con lo que tendría un polinomio interpolador de grado <= 4
    """
    puntos = list(range(1,6))

    """ Evaluamos con los puntos z """
    eval_z_newton = inewton_iter(puntos, [f(punto) for punto in puntos], z)
    eval_z_lagrange = ilangrange(puntos, [f(punto) for punto in puntos], z)

    pyplot.plot(z, f_z, 'g', label = "$f(x) = 1/x$")
    pyplot.plot(z, eval_z_newton, 'r', label = "$P_4(x)$ por Newton")
    pyplot.plot(z, eval_z_lagrange, 'b', label="$P_4(x)$ por Langrange")
    
    pyplot.title("Ejercicio 3")

    x1, x2, _, _ = pyplot.axis()
    pyplot.axis((x1, x2, -1, 1))
    pyplot.axhline(0, color='black')
    pyplot.axvline(0, color='black')
    pyplot.legend(loc="upper left")

    pyplot.show()


""" Ejercicio 4 """
def fenomeno_runge(n):
    """ Puntos para evaluar con nuestro polinomio interpolador """
    z = linspace(-1, 1, 200)

    """ Función de Runge """
    runge = lambda x : 1 / (1 + 25 * x**2)

    runge_z = [runge(z_i) for z_i in z]

    """ Puntos para evaluar """
    puntos = [ 2 * (i - 1) / n - 1 for i in range(1, n + 2) ]

    """ Evaluamos nuestro polinomio con puntos en z"""
    eval_z = inewton_iter(puntos, [runge(punto) for punto in puntos], z)

    pyplot.plot(z, runge_z, 'g', label = "$Runge_{25}(x) = 1/(1+25x^2)$")
    pyplot.plot(z, eval_z, 'r', label = "$P_{%s}(x)$"%n)

    pyplot.title("Ejercicio 4, $n = {%s}$"%n)

    x1, x2, _, _ = pyplot.axis()
    pyplot.axis((x1, x2, -1, 1))
    pyplot.axhline(0, color='black')
    pyplot.axvline(0, color='black')
    pyplot.legend(loc="upper left")

    pyplot.show()

def ej4():
    for n in range(1, 16):
        fenomeno_runge(n)

def ej4_alt():
    """ Puntos para evaluar con nuestro polinomio interpolador """
    z = linspace(-1, 1, 200)

    """ Función de Runge """
    runge = lambda x : 1 / (1 + 25 * x**2)

    runge_z = [runge(z_i) for z_i in z]

    """ Los siguiente deja en plots lo siguiente:
        (0,0) (0,1) (0,2) (0,3) (0,4)
        (1,0) (1,1) (1,2) (1,3) (1,4)
        (2,0) (2,1) (2,2) (2,3) (2,4)
    """

    pyplot.subplots_adjust(top=0.85)

    fig, plots = pyplot.subplots(3, 5)
    fig.tight_layout()

    for n in range(1, 16):
        """ Puntos para evaluar """
        puntos = [ ( 2 * (i - 1) / n ) - 1 for i in range(1, n + 2) ]
        """ Evaluamos nuestro polinomio con puntos en z"""
        eval_z = inewton_iter(puntos, [runge(punto) for punto in puntos], z)
        
        i = n // 5
        j = n %  5 - 1
        if j == -1:
            i -= 1
            j += 5

        plots[i, j].plot(z, runge_z, 'g')
        plots[i, j].plot(z, eval_z, 'r')
        
        plots[i, j].set_title("$n = {%s}, P_{%s}(x)$"%(n,n))
        x1, x2, _, _ = plots[i, j].axis()
        plots[i, j].axis((x1, x2, -2, 2))
        plots[i, j].axhline(0, color='black')
        plots[i, j].axvline(0, color='black')
    pyplot.show()

""" Ejercicio 5 """
def ej5():
    data = loadtxt(fname = "./Datos_Laboratorio_3/datos_aeroCBA.dat", encoding = "ascii")
    (n, _) = data.shape
    """ Datos son anuales
        Años
        x = [ data[i, 0] for i in range(n)]

        Temperatura media
        t_med = [ data[i, 1] for i in range(n)]
        
        Temperatura máxima
        t_max = [ data[i, 2] for i in range(n)]
        
        Temperatura mínima
        t_min = [ data[i, 3] for i in range(n)]
        
        Precipitaciones total y/o nieve derretida (mm)
        pp = [ data[i, 4] for i in range(n)]
        
        Velocidad media en Km/hora
        vel_med = [ data[i, 5] for i in range(n)]

        Total de días con lluvia
        dias_lluvia = [ data[i, 6] for i in range(n)]

        Total días con nieve
        dias_nieve = [ data[i, 7] for i in range(n)]

        Total días con tormenta
        dias_tormenta = [ data[i, 8] for i in range(n)]

        Total días con niebla
        dias_niebla = [ data[i, 9] for i in range(n)]
        
        Total días con tornados o embudos
        dias_tornados = [ data[i, 10] for i in range(n)]

        Total días con granizo
        dias_granizo = [ data[i, 11] for i in range(n)]
    """
    min_x = int(data[0, 0])
    max_x = int(data[n-1, 0])

    # Para decidir en nuestro for
    x = { data[i, 0]: data[i, 1] for i in range(n) }
    x_keys = x.keys()
    # Los años sin datos
    x_sin_datos = []
    # Los años con datos
    x_con_datos = []
    # Temp media anual
    t_med = []
    for a in range(min_x, max_x + 1):
        if a in x_keys and not isnan(x[a]):
            x_con_datos.append(a)
            t_med.append(x[a])
        else:
            x_sin_datos.append(a)
    
    # Para ver la curva, una muestra de 1000 puntos para usar con el spline
    x_space = linspace(min_x, max_x, 1000)

    spline = CubicSpline(x_con_datos, t_med, extrapolate=True)

    res_con_datos = dict(zip(x_con_datos, t_med))
    res_estimados = { float(i): spline(i).item() for i in x_sin_datos }
    
    pyplot.plot(x_con_datos, t_med, 'ob', label='Temp Media/Año dados')   
    pyplot.plot(x_sin_datos, spline(x_sin_datos), 'or', label="Temp Media/Año no dados")
    pyplot.plot(x_space, spline(x_space), 'g', label="Spline Cúbico con los datos")
    pyplot.title("Ejercicio 5")
    pyplot.legend(loc="upper right")

    pyplot.show()

    # Diccionario uniendo ambos diccionarios, ordenados
    # {**res_con_datos, **res_estimados}
    # Extraigo los valores y después lo devuelvo una lista
    return list(({**res_con_datos, **res_estimados}).values())
