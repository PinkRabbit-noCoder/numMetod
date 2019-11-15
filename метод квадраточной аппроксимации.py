import pylab
import numpy as np
import sympy
import math
def is_number(str): # проверка является ли строка числом типа float
    try:
        float(str)
        return True
    except ValueError:
        return False
def is_dot(str): # проверка есть ли в строке символы из массива
    znak=[',', '/','*','?',';',':','!','#','"','$','@','%','^']
    index=np.empty(len(znak))
    for i in np.arange(len(znak)):
        index[i] = str.find(znak[i])
    if index.all(-1):
        return True
    else: return False



def prov_v(c): # проверка является ли введенная строка числом, если нет то функция просит ввсести строку снова
    if is_number(c):
        c = float(c)
    else:
        while (not is_number(c)):
            if any(letter.isalpha() for letter in c): #проверка есть ли в строке буквы
                print('Ошибка: вы ввели не число! Вы ввели букву(ы). ')
                c = input('Bведите число! ')
            else:
                if is_dot(c):
                    print('Ошибка: не верный формат числа! Число должно иметь формат #.# ')
                    c = input('Bведите число! ')
                else:
                    if c == '':
                        print("Ошибка: вы ничего не ввели!")
                        c = input('Введите число')

        c = float(c)
    return (c)

print('Функция имеет вид : A(x - a)**2 + B(y - b)**2 + c*x*y')
A = prov_v(input('Введите коэффициент A '))
B = prov_v(input('Введите коэффициент B '))
a = prov_v(input('Введите коэффициент a '))
b = prov_v(input('Введите коэффициент b '))
c = prov_v(input('Введите коэффициент c '))
f = lambda x, y: A*((x - a)**2) + B*((y - b)**2) + c*x*y
gr= np.empty(2)
def g_x(): # частная производная по х
   x,y=sympy.symbols('x y')
   return(sympy.diff(f(x,y),x))
def g_y():# частная производная по у
   x,y=sympy.symbols('x y')
   return( sympy.diff(f(x,y), y))
def gess(x,y):
    x, y = sympy.symbols('x y')
    A= float(sympy.diff(sympy.diff(f(x,y),x), x))
    B =float(sympy.diff(sympy.diff(f(x,y),y), y))
    C= float(sympy.diff(sympy.diff(f(x,y),x), y))

    if A*B-C**2 >= 0:
        print('Функция имеет экстркмум')
        if A < 0:
           name ='точка максимума'
        else:
            if A > 0:
                name = 'точка минимума'
            else: name = 'точка экстремума'
    else:name = 'точка не экстремума'
    return name
def korn():# находит корни системы уравнений из частных производных
    x, y = sympy.symbols('x y')
    korni =[]
    for a in sympy.linsolve([g_x(), g_y()],(x,y)):
        for b in a:
           korni.append(float(b))
    comment = gess(korni[0], korni[1])
    return(comment,korni)

def graf(a,b):#построение графика
    comment, korni = korn()
    reng= np.max([math.fabs(korni[0]),math.fabs(korni[1]),math.fabs(a),math.fabs(b)])
    Yy= np.arange(-1*reng-10, reng+10, 0.1)
    Xx = np.arange(-1*reng-10,reng+10, 0.1)
    X, Y = np.meshgrid(Xx, Yy)
    pylab.figure(1)
    cs = pylab.contour(X, Y, f(X, Y))
    k = pylab.plot(korni[0], korni[1], 'o',color = "purple")
    pylab.clabel(cs, colors="black", fmt='x=%.2f')
    h = pylab.plot(a, b, 'r*')
    pylab.legend(['Истинная '+comment, 'Найденная '+comment])
    pylab.grid()
    pylab.show()
def gran():#корректность введенных границ аппроксимации
    gr[0]=prov_v((input('Введите левую границy аппроксимации ')))
    gr[1] = prov_v(float(input('Введите правую границу апроксимации ')))
    if gr[0]== gr[1]:
        while gr[0]== gr[1]:
            gr[1] = prov_v(float(input('Левая и правая граница должны отличаться \n Введите  другую границу аnпроксимации ')))
    return(gr)
def approxi(con, comment):
    if any(con in i for i in ['x', 'X', 'х', 'Х']):
        x = prov_v((input('Введите значение, на котором хотите зафиксировать переменную х ')))
        gr = gran()
        f1 = f(x, gr[0])
        f2 = f(x, sum(gr) / 2)
        f3 = f(x, gr[1])
        a0 = f1
        a1 = (f2 - f1) / ((sum(gr) / 2) - gr[0])
        a2 = (1 / (gr[1] - (sum(gr) / 2))) * (((f3 - f1) / (gr[1] - gr[0])) - ((f2 - f1) / ((sum(gr) / 2) - gr[0])))
        y_opt = (((sum(gr) / 2) + gr[0]) / 2) - (a1 / 2 * a2)

        print("Параметры аппроксимации равны а0 =",a0,"а1 =",a1,"а2 =",a2)
        print(comment+' находиться в  х =', x, ' и у =', y_opt, ', функция в этой точке равена ',
              f(x, y_opt))

        graf(x, y_opt)
    else:

        if any(con in i for i in ['y', 'Y', 'у', 'У']):
            y = prov_v((input('Введите значение, на котором хотите зафиксировать переменную у ')))
            gr = gran()
            f1 = f(gr[0], y)
            f2 = f(sum(gr) / 2, y)
            f3 = f(gr[1], y)
            a0 = f1
            a1 = (f2 - f1) / ((sum(gr) / 2) - gr[0])
            a2 = (1 / (gr[1] - (sum(gr) / 2))) * (((f3 - f1) / (gr[1] - gr[0])) - ((f2 - f1) / ((sum(gr) / 2) - gr[0])))
            x_opt = (((sum(gr) / 2) + gr[0]) / 2) - (a1 / 2 * a2)
            print("Параметры аппроксимации равны а0 =", a0, "а1 =", a1, "а2 =", a2)
            print(comment+' находиться в х =', x_opt, ' и у =', y, ', функция в этой точке равена ',
                  f(x_opt, y))
            graf(x_opt, y)
comment, korni = korn()
print('Истинная',comment,' находиться в ',korni)
con = input('Введите переменную, которую хотите зафиксировать ')
if any(con in i for i in ['x', 'X', 'х', 'Х', 'y', 'Y', 'у', 'У']):
    approxi(con, comment)
else:
    while not (any(con in i for i in ['x', 'X', 'х', 'Х', 'y', 'Y', 'у', 'У'])):
        print('Переменая для фиксации указана не верно или не выбрана ')
        con = input('Введите переменную, которую хотите зафиксировать ')
    approxi(con, comment)
input('\n Нажмите Enter для выхода ')
