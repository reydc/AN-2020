from importlib  import reload
from inspect    import signature
from matplotlib import pyplot
from math       import tan, exp
from numpy      import sign, linspace
from sympy      import sympify, lambdify
from warnings   import catch_warnings

""" Ejercicio 1 """

def rbisec(fun, I, err, mit):
    """ fun: es la función sobre la que aplicar el método
        I:   es un intervalo de la forma [a,b]
        err: es la tolerancia deseada
        mit: es el número de iteraciones permitido
    """
    hx,hf = [],[]
    a, b = I
    u = fun(a)
    v = fun(b)
    if sign(u) == sign(v):
        print("Tienen el mismo signo: f({}) = {}, f({}) = {}...\n".format(a, u, b, v))
    it = 1
    e = b - a
    e /= 2.
    x = a + e
    w = fun(x)
    hx.append(x)
    hf.append(w)
    while it <= mit and abs(w) >= err:
        if sign(w) != sign(u):
            b = x
            v = w
        else:
            a = x
            u = w
        e /= 2
        x = a + e
        w = fun(x)
        hx.append(x)
        hf.append(w)
        it += 1
    if abs(w) < err:
        print("Converge por f({}) ~ {}\n".format(x, w))
        print("Converge a las {} iteraciones (de las {} iteraciones dadas).\n".format(it, mit))
    return hx,hf


""" Ejercicio 2 """
"""
a) Encontrar la menor solución positiva para f(x) = tan(x) - 2x
   con un error menor a 10^(-5) en menos de 100 iteraciones. ¿Cuántas 
   iteraciones son necesarias cuando comenzamos con I = [0.8,1.4]?
   Usar la sintaxis: hx, hy = rbisec(fun_lab2ej2a, I, 1e-5,100).
b) Encontrar una aproximación a sqrt(3) con un error menor a 10^(-5),
   considerando la función "f(x) = x^2 - 3" que debe llamarse fun_lab2ej2b.
c) Graficar las dos funciones de a) y b) y los pares (xk,f(xk)) y con 
   al menos dos intervalos iniciales distintos para cada uno.
"""

fun_lab2ej2a = lambda x : tan(x) - 2*x

fun_lab2ej2b = lambda x : x**2 - 3

def fun_lab2ej2():
    
    """ Intervalos para fun_lab2ej2a """
    ia1 = [0.8 , 1.4]
    ia2 = [-1 , 0.5]

    hx_ej2a_ia1, hf_ej2a_ia1 = rbisec(fun_lab2ej2a, ia1, 1e-5, 100)
    hx_ej2a_ia2, hf_ej2a_ia2 = rbisec(fun_lab2ej2a, ia2, 1e-5, 100)

    """ Intervalos para fun_lab2ej2b """
    ib1 = [0.0 , 3.0]
    ib2 = [-4.0 , 0.0]
    
    hx_ej2b_ib1, hf_ej2b_ib1 = rbisec(fun_lab2ej2b, ib1, 1e-5, 100)
    hx_ej2b_ib2, hf_ej2b_ib2 = rbisec(fun_lab2ej2b, ib2, 1e-5, 100)

    l_space = linspace(-5, 5, 600)

    fun_lab2ej2a_completa = list(map(fun_lab2ej2a, l_space))
    fun_lab2ej2b_completa = list(map(fun_lab2ej2b, l_space))
    
    pyplot.plot(l_space, fun_lab2ej2a_completa, 'g', label = "fun_lab2ej2a")
    pyplot.plot(l_space, fun_lab2ej2b_completa, 'r', label = "fun_lab2ej2b")

    pyplot.plot(hx_ej2a_ia1, hf_ej2a_ia1, '.--b', \
                label = "rbisec fun_lab2ej2a [{} , {}]".format(*ia1))
    pyplot.plot(hx_ej2a_ia2, hf_ej2a_ia2, '.--b', \
                label = "rbisec fun_lab2ej2a [{} , {}]".format(*ia2))

    pyplot.plot(hx_ej2b_ib1, hf_ej2b_ib1, '.:k', \
                label = "rbisec fun_lab2ej2b [{} , {}]".format(*ib1))
    pyplot.plot(hx_ej2b_ib2, hf_ej2b_ib2, '.:k', \
                label = "rbisec fun_lab2ej2b [{} , {}]".format(*ib2))

    x1, x2, _, _ = pyplot.axis()
    pyplot.axis((x1, x2, -1, 1))
    pyplot.axhline(0, color='black')
    pyplot.axvline(0, color='black')
    pyplot.legend(loc="upper left")

    pyplot.show()

""" Ejercicio 3 """

""" Se puede usar el método de Newton como :
    f, fp = obtener_fun(<String de Expresión>)
    fun = lambda x : (f(x),fp(x))
    hx, hf = rnewton(fun, x0, err, mit)

    Otra forma:
    hx, hf = rnewton(hacer_fun(<String de Expresión>), x0, err, mit)
"""
def obtener_fun(str_f):
    """ str_f:     es un string que representa una función
        Devuelvo dos lambdas que pueden ser usadas para evaluar la
        función que dimos representada como un string y su derivada,
        respectivamente
    """
    try:
        """ Uso sympy para la derivada, por lo tanto, lo que sea que
            que haya dado como string debe ser derivable
        """
        sym_expr = sympify(str_f)
        sym_expr_prima = sym_expr.diff()
        print("Se han generado:")
        print("f = {}".format(sym_expr))
        print("    símbolos = {}".format(sym_expr.free_symbols))
        print("f' = {}".format(sym_expr_prima))
        print("    símbolos = {}".format(sym_expr_prima.free_symbols))
        print("")
        """ A lo sumo, f' va a tener tantas variables como f"""
        return lambdify(sym_expr.free_symbols, sym_expr),\
               lambdify(sym_expr_prima.free_symbols, sym_expr_prima)
    except Exception as e:
        print(e)

""" Observar que esta función es más general de lo necesario """
def hacer_fun(str_f):
    """ str_f: es un string que representa una función
        Devuelve una función para la cual dando los puntos a evaluar,
        evalua la función dada por el string y su derivada
    """
    try:
        f,fp = obtener_fun(str_f)
        """ Sólo toma los elementos necesarios para evaluar cada función """
        return lambda *args : (f(*args[0:len(signature(f).parameters)]), fp(*(args[0:len(signature(fp).parameters)]))) 
    except Exception as e:
        print(e)

""" Probar haciendo haciendo en la consola:
    lab2.rnewton(lab2.hacer_fun("x**2-x-2"), 1, 1e-9, 10)
    lab2.rnewton(lab2.hacer_fun("x**3-2*x**2+x-3"), 3, 1e-9, 10)
"""

def rnewton(fun, x0, err, mit):
    """ fun:  es una función que dado x, retorna f(x), f'(x) 
        x0:   es el punto inicial
        err:  es la tolerancia deseada
        mit:  es el número de iteraciones permitido
    """
    hx,hf = [],[]
    x_prev = x0
    f,fp = fun(x_prev)
    it = 1
    e = 1.
    hx.append(x_prev)
    hf.append(f)
    while it <= mit and abs(f) >= err and e >= err:
        x_sig = x_prev - (f/fp)
        e = abs(x_sig - x_prev) / abs(x_sig)
        x_prev = x_sig
        f,fp = fun(x_prev)
        hx.append(x_prev)
        hf.append(f)
        it += 1
    if abs(f) < err:
        print("Converge por f({}) ~ {}\n".format(x_prev, f))
        print("Converge a las {} iteraciones (de {} iteraciones dadas).\n".format(it, mit))
    return hx,hf

""" Ejercicio 4 """
""" Escribir una función que ingresando a > 0, retorne una aproximación de su
    raíz cúbica. La aproximación debe realizarse usando el método de Newton
    para resolver "x^3-a = 0" con un error menor a 10^(-6) mediante el uso de la
    función "f(x) = x^3 - a".

    Probar haciendo en la consola:
    lab2.fun_lab2ej4(3,3,30)
"""

def fun_lab2ej4(a, x0, mit):
    if a > 0:
        print("Entrada: a = {}, x0 = {}, mit = {}\n".format(a, x0, mit))
        hx, _ = rnewton(hacer_fun("x**3-{}".format(a)), x0, 1e-6, mit)
        return hx[len(hx) - 1]
    else:
        print("Valor de entrada <= 0\n")

""" Ejercicio 5 """

""" Probar haciendo en la consola:
    lab2.ripf(lambda x:1+(2/x), 1, 1e-6,30)
    lab2.ripf(lambda x:1+(2/x), 1, 1e-9,30)
    lab2.ripf(lambda x:1+(2/x), 1, 1e-16,100)
    El próximo da el valor correcto:
    lab2.ripf(lambda x:1+(2/x), 1, 1e-17,100)
"""

def ripf(fun, x0, err, mit):
    """ fun: es la función para la que se desea hallar el punto fijo,
             sería el g(x) en el teórico
        x0:  es el valor inicial
        err: tolerancia permitida
        mit: número de iteraciones permitido
    """
    hx = []
    x_prev = x0
    x_sig  = fun(x_prev)
    hx.append(x_prev)
    it = 1
    while it <= mit and abs(x_sig - x_prev) > err:
        x_prev = x_sig
        x_sig  = fun(x_prev)
        hx.append(x_prev)
        it += 1
    if abs(x_sig - x_prev) < err:
        print("Converge por f({}) ~ {}\n".format(x_prev, x_sig))
        print("Converge a las {} iteraciones (de las {} iteraciones dadas).\n".format(it, mit))
    return hx

""" Ejercicio 6 """
""" Usar la fórmula x(n+1) = 2^(x(n)-1) para resolver 2*x = 2^x.
    Utilizar la función de iteración por punto fijo para ver si 
    converge y en caso afirmativo estudiar hacia qué valores lo
    hace para distintas elecciones de x0, tomando mit = 100 y
    err = 10^(-5). 
"""

def investigar_puntos_fijos(fun, I, puntos_intervalo, err, mit, graficar = False):
    """ I:                intervalo de la forma [a, b]
        puntos_intervalo: la cantidad de puntos iniciales en 
                          el intervalo
    """
      
    puntos = linspace(*I, puntos_intervalo)

    if graficar:
        pyplot.plot(puntos, list(map(fun, puntos)), 'g', label="f")

    print("Puntos:")
    print(str(puntos))
    print("\n" + "-" * 60 + "\n")
    
    """ Puntos iniciales donde se itera el método """
    puntos_iteran = []
    """ Puntos iniciales que nos llevan a warnings o a excepciones """
    puntos_problematicos  = []
    
    with catch_warnings():
        for i in puntos:
            print("x0 = {}".format(i))
            try:
                _ = ripf(fun , i, err, mit)
                puntos_iteran.append(i)
            except Exception as e:
                print("\nATENCIÓN: Algo ocurrió en tiempo de ejecución")
                print(e)
                puntos_problematicos.append(i)
            print("\n" + "-" * 60 + "\n")
    
    if graficar:
        pyplot.plot(puntos_iteran, \
                    list(map(fun, puntos_iteran)), \
                    'ob', label="Puntos ini. que iteran")
        pyplot.plot(puntos_problematicos, \
                    list(map(fun, puntos_problematicos)), \
                    'or', label="Puntos ini. que problemáticos")

        pyplot.axhline(0, color='black')
        pyplot.axvline(0, color='black')
        pyplot.legend(loc="upper left")
    
        pyplot.show()

""" Nota: En el programa hay puntos que no convergen hacía el punto
    fijo, sino que divergen y producen overflow
    En este caso resulta que x == 1 es un punto fijo atractor (el valor
    absoluto de la derivada de la función en el punto es menor a 1) y
    x == 2 es un punto fijo repelente
"""
def fun_lab2ej6():
    fun = lambda x : 2**(x-1)
    investigar_puntos_fijos(fun, [-10,10], 10, 1e-5, 100, True)

""" Ejercicio 7 """
""" Se desea conocer la gráfica de una función u tal que u(x) = y,
    donde y es solución de "y - exp(-(1-x*y)^2) = 0".
    Implementar tres versiones de esta función, hallando el valor 
    de y con los métodos de dados.
    Los valores iniciales y tolerancias usadas por los distintos 
    métodos deben ser escogidos de manera que cualquier usuario
    pueda graficar u en [0.0 , 1.5] sin inconvenientes.
"""

""" Para poder buscar las raíces que nos hacen falta definimos
    la siguiente función que fija a x
"""
""" Para Bisección """
def fi(x):
    return lambda y : y - exp(-(1-x*y)**2)

""" Para Newton """
def str_fi(x):
    return "y - exp(-(1-%s*y)**2)"%(x)

""" Para Iteración de punto fijo """
def fi_ipf(x):
    return lambda y : exp(-(1-x*y)**2)

def graficar_fi_x(Iy, num_puntos_y, Ix, num_puntos_x, graficar = False):
    
    puntos_y = linspace(*Iy, num_puntos_y)
    puntos_x = linspace(*Ix, num_puntos_x)

    for x in puntos_x:
        fi_x = fi(x)
        h = list(map(fi_x, puntos_y))

        if graficar:
            pyplot.plot(puntos_y, h, '--g', label="$\Phi_{%s}(y)$"%(x))
    
    if graficar:
        pyplot.title("Funciones $\Phi_x(y) = y - e^{-(1-xy)^2}$")
        pyplot.axhline(0, color='black')
        pyplot.axvline(0, color='black')
        pyplot.ylabel("$\Phi_x(y)$")
        pyplot.xlabel("$y$")
        pyplot.legend(loc="upper left")
        pyplot.show()

""" Probar haciendo:
    lab2.ver_fi_ej7(-10, 10, 100, -2, 5, 10)
"""
def ver_fi_ej7(y_a, y_b, num_puntos_y, x_a, x_b, num_puntos_x):
    graficar_fi_x([y_a,y_b], num_puntos_y, [x_a,x_b], num_puntos_x, True)


def fun_lab2ej7(err_bisec = 1e-9, it_bisec = 100, err_newton = 1e-9, it_newton = 100, err_ipf = 1e-9, it_ipf = 100):
    Iy = [-10 , 10]
    Ix = [0 , 1.5]
    puntos_x = linspace(*Ix, 30)
    
    hx_bisec = []
    hu_bisec = []

    hx_newton = []
    hu_newton = []

    hx_ipf = []
    hu_ipf = []

    for x in puntos_x:
        print("\n" + "-"*60)
        print("x = " + str(x))
        fi_x     = fi(x)
        str_fi_x = hacer_fun(str_fi(x))
        fi_ipf_x = fi_ipf(x)

        print("\nMétodo Bisección:\n")
        # h_bisec_y, h_bisec_f
        h_bisec_y, _ = rbisec(fi_x, Iy, err_bisec, it_bisec)
        len_bisec = len(h_bisec_y)
        if  len_bisec < it_bisec:
            hx_bisec.append(x)
            hu_bisec.append(h_bisec_y[len_bisec - 1])
        
        print("\nMétodo de Newton:\n")
        # h_newton_y, h_newton_f
        h_newton_y, _ = rnewton(str_fi_x, x, err_newton, it_newton)
        len_newton = len(h_newton_y)
        if len_newton < it_newton:
            hx_newton.append(x)
            hu_newton.append(h_newton_y[len_newton - 1])
        
        print("\nMétodo del punto fijo:\n")
        # h_ipf_y
        h_ipf_y = ripf(fi_ipf_x, x, err_ipf, it_ipf)
        len_ipf = len(h_ipf_y)
        if len_ipf < it_ipf:
            hx_ipf.append(x)
            hu_ipf.append(h_ipf_y[len_ipf - 1])
    
    fig, (p1, p2, p3) = pyplot.subplots(1, 3)

    fig.suptitle("Ejercicio 7")

    p1.plot(hx_bisec, hu_bisec, "--", color="royalblue")
    p1.set_title("$u(x) = y$ por rbisec")
    p1.axhline(0, color='black')
    p1.axvline(0, color='black')

    p2.plot(hx_newton, hu_newton, "--", color="red")
    p2.set_title("$u(x) = y$ por rnewton")
    p2.axhline(0, color='black')
    p2.axvline(0, color='black')

    p3.plot(hx_ipf, hu_ipf, "--", color="forestgreen")
    p3.set_title("$u(x) = y$ por ripf")
    p3.axhline(0, color='black')
    p3.axvline(0, color='black')

    pyplot.show()