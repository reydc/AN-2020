from importlib  import reload
from matplotlib import pyplot
from scipy      import integrate
from sympy      import sympify, symbols, latex
from numpy      import linspace, vectorize, sin, cos, tan, exp, log, pi, ceil

def intenumcomp(fun, a, b, N, regla):
    if b < a:
        print("[intenumcomp] Se queire especificar un intervalo [a,b], pero b < a\n")
        return None
    if isinstance(N, int):
        if N <= 0:
            print("[intenumcomp] N debe ser positivo\n")
            return None
        else:
            if regla == "trapecio":
                h = (b - a) / N
                f = [ fun(a + j*h) for j in range(1, N) ]
                return h/2 * (fun(a) + fun(b) + 2 * sum(f) )
            elif regla == "pm":
                if N % 2:
                    print("[intenumcomp] N debe ser par para usar la regla compuesta del Punto Medio\n")
                    return None
                if N <= 2:
                    print("[intenumcomp] N > 2 para usar la regla compuesta del Punto Medio\n")
                    return None
                h = (b - a) / N
                f = [ fun(a + (2 * j + 1) * h) for j in range(0, (N-2)//2 + 1) ]
                return 2 * h * sum(f)
            elif regla == "simpson":
                if N % 2:
                    print("[intenumcomp] N debe ser par para usar la regla compuesta de Simpson\n")
                    return None
                h = (b - a) / N
                f_1 = [ fun(a + 2*j*h) for j in range(1, N//2) ]
                f_2 = [ fun(a + (2*j - 1)*h) for j in range(1, N//2 + 1) ]
                return h/3 * (fun(a) + fun(b) + 2 * sum(f_1) + 4 * sum(f_2))
            else:
                print("[intenumcomp] No es una regla programada, las programadas son \"trapecio\", \"pm\" y \"simpson\"\n")
                return None
    else:
        print("[intenumcomp] N no es un entero\n")
        return None

def ej2():
    val = 1 - 1 / exp(1)
    fun = lambda x: exp(-x)
    """ Con la regla del Trapecio """
    print("Ejercicio 2: f(x) = e**(-x)\n")
    print("Error con la regla compuesta del Trapecio, con N = 4: %s\n"%(\
        abs(val - intenumcomp(fun, 0, 1, 4, "trapecio")) ))
    print("Error con la regla compuesta del Trapecio, con N = 10: %s\n"%(\
        abs(val - intenumcomp(fun, 0, 1, 10, "trapecio")) ))
    print("Error con la regla compuesta del Trapecio, con N = 20: %s\n"%(\
        abs(val - intenumcomp(fun, 0, 1, 20, "trapecio")) ))
    
    """ Con la regla del Punto Medio """
    print("Error con la regla compuesta del Punto Medio, con N = 4: %s\n"%(\
        abs(val - intenumcomp(fun, 0, 1, 4, "pm")) ))
    print("Error con la regla compuesta del Punto Medio, con N = 10: %s\n"%(\
        abs(val - intenumcomp(fun, 0, 1, 10, "pm")) ))
    print("Error con la regla compuesta del Punto Medio, con N = 20: %s\n"%(\
        abs(val - intenumcomp(fun, 0, 1, 20, "pm")) ))
    
    """ Con la regla de Simpson """
    print("Error con la regla compuesta del Simpson, con N = 4: %s\n"%(\
        abs(val - intenumcomp(fun, 0, 1, 4, "simpson")) ))
    print("Error con la regla compuesta del Simpson, con N = 10: %s\n"%(\
        abs(val - intenumcomp(fun, 0, 1, 10, "simpson")) ))
    print("Error con la regla compuesta del Simpson, con N = 20: %s\n"%(\
        abs(val - intenumcomp(fun, 0, 1, 20, "simpson")) ))

def senint(x):
    N = ceil([ 10 * v_x for v_x in x ])
    N = list(map(int, N))
    N = list(map(lambda n: n if n > 0 else (n + 1), N))
    y = []
    fun = lambda t: cos(t)
    for i in range(len(x)):
        y.append(intenumcomp(fun, 0, x[i], N[i], "trapecio"))
    return y

def ej3():
    x = []
    last = 0
    x.append(last)
    while last <= 2*pi:
        last += 0.5
        x.append(last)
    
    x_p = linspace(0, 7, 100)
    pyplot.plot(x_p, sin(x_p), "g", label="$sin(x)$")
    pyplot.plot(x, senint(x), color="slategray", label="$senint(x)$")
    pyplot.title("Ejercicio 3")
    pyplot.legend(loc="upper left")
    pyplot.axhline(0, color="black")
    pyplot.axvline(0, color="black")
    pyplot.show()

""" Para el próximo ejercicio queremos calcular la integral con un cierto error de
    tolerancia. Entonces, siendo M una cota del máximo valor posible en [a,b]
    correspondiente:
    Valor absoluto del error para Trapecio = (b-a)**3 * abs(M) / (12 * N) 
    Valor absoluto del error para Simpson  = (b-a)**5 * abs(M) / (180 * N)
    Luego, para asegurar una tolerancia del error de 10**(-5) necesito:
    Para Trapecio: N >= (b-a)**3 * abs(M) * 10**5 / 12
    Para Simpson:  N >= (b-a)**5 * abs(M) * 10**5 / 180
    Con esto se pueden hacer los cálculos, que son más o menos parecidos
"""

def ej4a():
    """ El valor exacto de la integral es 1 - 2 / exp(1) """
    fun = lambda x : x * exp(-x)
    
    derivadas = [ sympify("x * exp(x)") ]
    for i in range(1, 5):
        derivadas.append(derivadas[i - 1].diff())
    for i in range(0, 5):
        print("f_%s(x) = %s\n"%(i, derivadas[i]))
    
    I = linspace(0, 1, 1000)
    x = symbols("x")
    f_2_vect = vectorize(lambda v: derivadas[2].evalf(subs={x : v}))
    f_2_label = "$f^{(2)}(x) = %s$"%(latex(derivadas[2]))
    f_4_vect = vectorize(lambda v: derivadas[4].evalf(subs={x : v}))
    f_4_label = "$f^{(4)}(x) = %s$"%(latex(derivadas[4]))
    pyplot.plot(I, f_2_vect(I), "g", label=f_2_label)
    pyplot.plot(I, f_4_vect(I), color="slateblue", label=f_4_label)
    pyplot.title("Ejercicio 4.a")
    pyplot.legend(loc="upper left")
    pyplot.axhline(0, color="black")
    pyplot.axvline(0, color="black")
    pyplot.show()
    
    print("Ejercicio 4.a: f(x) = x*e^(-x)\n")
    f_2_max = f_2_vect(1)
    f_4_max = f_4_vect(1)
    print("La segunda derivada alcanza el máximo en 1, en [0,1], con valor %s\n"%f_2_max)
    print("La cuarta derivada alcanza el máximo en 0, en [0,1], con valor %s\n"%f_4_max)
    
    N = 1
    while N < f_2_max * 10**5 / 12:
        N +=1
    val_trap = intenumcomp(fun, 0, 1, N, "trapecio")
    print("N = %s\n"%N)
    print("T = %s\n"%val_trap)
    N = 2
    while N < f_4_max * 10**5 / 180:
        N += 2
    if N%2:
        N += 1
    val_simp = intenumcomp(fun, 0, 1, N, "simpson")
    print("N = %s\n"%N)
    print("S = %s\n"%val_simp)
    
    return val_trap, val_simp

def ej4b():
    """ El valor exacto de la integral es sin(1) - cos(1) """
    fun = lambda x : x * sin(x)
    
    derivadas = [ sympify("x * sin(x)") ]
    for i in range(1, 5):
        derivadas.append(derivadas[i - 1].diff())
    for i in range(0, 5):
        print("f_%s(x) = %s\n"%(i, derivadas[i]))
    
    I = linspace(0, 1, 1000)
    x = symbols("x")
    f_2_vect = vectorize(lambda v: derivadas[2].evalf(subs={x : v}))
    f_2_label = "$f^{(2)}(x) = %s$"%(latex(derivadas[2]))
    f_4_vect = vectorize(lambda v: derivadas[4].evalf(subs={x : v}))
    f_4_label = "$f^{(4)}(x) = %s$"%(latex(derivadas[4]))
    pyplot.plot(I, f_2_vect(I), "g", label=f_2_label)
    pyplot.plot(I, f_4_vect(I), color="slateblue", label=f_4_label)
    pyplot.title("Ejercicio 4.b")
    pyplot.legend(loc="upper right")
    pyplot.axhline(0, color="black")
    pyplot.axvline(0, color="black")
    pyplot.show()

    print("Ejercicio 4.b: f(x) = x*sen(x)\n")
    f_2_max = f_2_vect(0)
    f_4_max = abs(f_4_vect(0)) # < 0
    print("La segunda derivada alcanza el máximo en 1, en [0,1], con valor %s\n"%f_2_max)
    print("La cuarta derivada alcanza el máximo en 0, en [0,1], con valor %s\n"%f_4_max)

    N = 1
    while N < f_2_max * 10**5 / 12:
        N +=1
    val_trap = intenumcomp(fun, 0, 1, N, "trapecio")
    print("N = %s\n"%N)
    print("T = %s\n"%val_trap)
    N = 2
    while N < f_4_max * 10**5 / 180:
        N += 2
    if N%2:
        N += 1
    val_simp = intenumcomp(fun, 0, 1, N, "simpson")
    print("N = %s\n"%N)
    print("S = %s\n"%val_simp)
    
    return val_trap, val_simp

def ej4c():
    fun = lambda x: (1 + x**2)**(3/2)
    derivadas = [ sympify("(1+x**2)**(3/2)") ]
    for i in range(1, 5):
        derivadas.append(derivadas[i - 1].diff())
    for i in range(0, 5):
        print("f_%s(x) = %s\n"%(i, derivadas[i]))
    
    I = linspace(0, 1, 1000)
    x = symbols("x")
    f_2_vect = vectorize(lambda v: derivadas[2].evalf(subs={x : v}))
    f_2_label = "$f^{(2)}(x) = %s$"%(latex(derivadas[2]))
    f_4_vect = vectorize(lambda v: derivadas[4].evalf(subs={x : v}))
    f_4_label = "$f^{(4)}(x) = %s$"%(latex(derivadas[4]))
    pyplot.plot(I, f_2_vect(I), "g", label=f_2_label)
    pyplot.plot(I, f_4_vect(I), color="slateblue", label=f_4_label)
    pyplot.title("Ejercicio 4.c")
    pyplot.legend(loc="upper right")
    pyplot.axhline(0, color="black")
    pyplot.axvline(0, color="black")
    pyplot.show()

    print("Ejercicio 4.c: f(x) = (1+x**2)**(3/2)\n")
    f_2_max = f_2_vect(1)
    f_4_max = f_4_vect(0)
    print("La segunda derivada alcanza el máximo en 1, en [0,1], con valor %s\n"%f_2_max)
    print("La cuarta derivada alcanza el máximo en 0, en [0,1], con valor %s\n"%f_4_max)

    N = 1
    while N < f_2_max * 10**5 / 12:
        N +=1
    val_trap = intenumcomp(fun, 0, 1, N, "trapecio")
    print("N = %s\n"%N)
    print("T = %s\n"%val_trap)
    N = 2
    while N < f_4_max * 10**5 / 180:
        N += 2
    if N%2:
        N += 1
    val_simp = intenumcomp(fun, 0, 1, N, "simpson")
    print("N = %s\n"%N)
    print("S = %s\n"%val_simp)
    
    return val_trap, val_simp

def ej4d():
    fun = lambda x : 1 / (1 - (sin(x)**2)/2)**(1/2)
    derivadas = [ sympify("1 / (1 - (sin(x)**2) / 2)**(1/2)") ]
    for i in range(1, 5):
        derivadas.append(derivadas[i - 1].diff())
    for i in range(0, 5):
        print("f_%s(x) = %s\n"%(i, derivadas[i]))
    
    I = linspace(0, pi/2, 1000)
    x = symbols("x")
    f_2_vect = vectorize(lambda v: derivadas[2].evalf(subs={x : v}))
    f_2_label = "$f^{(2)}(x) = %s$"%(latex(derivadas[2]))
    f_4_vect = vectorize(lambda v: derivadas[4].evalf(subs={x : v}))
    f_4_label = "$f^{(4)}(x) = %s$"%(latex(derivadas[4]))
    pyplot.plot(I, f_2_vect(I), "g", label=f_2_label)
    pyplot.plot(I, f_4_vect(I), color="slateblue", label=f_4_label)
    pyplot.title("Ejercicio 4.d")
    pyplot.legend(loc="upper left")
    pyplot.axhline(0, color="black")
    pyplot.axvline(0, color="black")
    pyplot.show()

    print("Ejercicio 4.d: f(x) = 1 / (1 - (sin(x)**2) / 2)**(1/2)\n")
    f_2_max = f_2_vect(0)
    f_4_max = f_4_vect(pi/2)
    print("La segunda derivada alcanza el máximo en 1, en [0, pi/2], con valor %s\n"%f_2_max)
    print("La cuarta derivada alcanza el máximo en 0, en [0, pi/2], con valor %s\n"%f_4_max)
    N = 1
    while N < (pi/2)**3 * f_2_max * 10**5 / 12:
        N +=1
    val_trap = intenumcomp(fun, 0, pi/2, N, "trapecio")
    print("N = %s\n"%N)
    print("T = %s\n"%val_trap)
    N = 2
    while N < (pi/2)**5 * f_4_max * 10**5 / 180:
        N += 2
    if N%2:
        N += 1
    val_simp = intenumcomp(fun, 0, pi/2, N, "simpson")
    print("N = %s\n"%N)
    print("S = %s\n"%val_simp)
    
    return val_trap, val_simp

""" El próximo ejercicio es integrar usando el módulo scipy.integrate """

def ej5a():
    """
    f(x) = exp(-x**2) , f(-x) = exp(-(-x)**2) = f(x) => exp es par
    Una forma de integrar sería:
    integral(-inf,+inf) f(x)dx = 2 * integral(0,+inf) f(x)dx
    También tenemos que 
    u ->  pi/2 <=> tan(u) -> +inf
    u -> -pi/2 <=> tan(u) -> -inf
    Si x = tan(u), u -> +pi/2, x -> +inf
                   u -> -pi/2, x -> -inf
    -x**2 = -tan(u)**2
    dx = sec(u)**2 * du = cos(u)**(-2) du
    """
    fun = vectorize(lambda u: exp(-tan(u)**2) * cos(u)**(-2))
    u = linspace(-pi/2, pi/2, 100)
    print("Ejercicio 5.a\n")
    trapecio = integrate.trapz(fun(u), u)
    simpson  = integrate.simps(fun(u), u, even="avg")
    print("Integral por regla del Trapecio (integrate.trapz): %s\n"%trapecio)
    print("Integral por regla de Simpson (integrate.simps): %s\n"%simpson)
    return trapecio, simpson

def ej5b():
    fun = vectorize(lambda x : (x**2) * log(x + (x**2 + 1)**(1/2)))
    x = linspace(0, 2, 100)
    print("Ejercicio 5.b\n")
    trapecio = integrate.trapz(fun(x), x)
    simpson  = integrate.simps(fun(x), x, even="avg")
    print("Integral por regla del Trapecio (integrate.trapz): %s\n"%trapecio)
    print("Integral por regla de Simpson (integrate.simps): %s\n"%simpson)
    return trapecio, simpson

def pendulo(l, alfa):
    """ l es la longitud del péndulo
        alfa es la amplitud del mismo 
        Esta función devuelve el período del péndulo
    """
    if 0 > alfa or alfa > 90:
        print("alfa no está en el rango [0, 90]\n")
        return None
    alfa = (pi/180) * alfa
    sub_T = lambda theta : 1 / (1 - sin(alfa/2)**2 * sin(theta)**2)**(1/2)
    """ c = 4 * (l/g)**(1/2), [g] = m/s**2, [l] = m """
    c = 4 * (l / 9.8)**(1/2)
    """ Se devuelve una magnitud del período """
    return c * intenumcomp(sub_T, 0, pi/2, 10, "simpson")

def ej6(l, n):
    """ l es la longitud del péndulo [m]
        n es la cantidad de puntos entre [0, 90] que se desean
        Acá solamente graficamos para ver el comportamiento
    """
    if not isinstance(n, int):
        print("[ej6] n no es entero\n")
        return None
    if n <= 1:
        print("[ej6] n <= 1, necesitamos al menos dos puntos para comparar\n")
        return None
    """ alfa [grados] """
    alfas = linspace(0, 90, n)
    pendulo_vect = vectorize(lambda alfa: pendulo(l, alfa))
    res = pendulo_vect(alfas)
    pyplot.plot(alfas, res, "g", label="$T_{l}(\\alpha), n = %s$"%n)
    pyplot.title("Ejercicio 6")
    pyplot.legend(loc="upper left")
    pyplot.axhline(0, color="black")
    pyplot.axvline(0, color="black")
    pyplot.show()
    
    return res
