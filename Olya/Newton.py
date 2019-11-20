import pylab
import numpy as np
import sympy
import math
def is_number(str): # проверка является ли строка числом типа float
    try:#пробуем привезти строку к типу флоат
        float(str)
        return True #получилось,значит возвращаем тру
    except ValueError:
        return False #не получилось возвращаем фолз
def is_dot(str): # проверка есть ли в строке символы из массива
    znak=[',', '/','*','?',';',':','!','#','"','$','@','%','^']
    index=np.empty(len(znak))
    for i in np.arange(len(znak)):
        index[i] = str.find(znak[i]) #проверяем наличние в стоке символов из массива и записываетм их индекс
    if index.all(-1):# если знака нет в строке то его индекс -1, если все индексы = -1 то в строке нет ни одного символла из массива
        return True
    else: return False
def prov_v(c): # проверка является ли введенная строка числом, если нет то функция просит ввсести строку снова
    if is_number(c):
        c = float(c)#если строка сразу приводится к числу, то приводим к числу
    else:#выдаем ошибку до тех пока пока введеная строка не приведется к числу
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

print('Функция имеет вид : (x - a)**2 + (y - b)**2 + c*x*y')

a = prov_v(input('Введите коэффициент a '))
b = prov_v(input('Введите коэффициент b '))
c = prov_v(input('Введите коэффициент c '))
f = lambda x, y: (x - a)**2 + (y - b)**2 + c*x*y

x= np.empty([2,1])#массив с найденными точками
x[0, 0]=prov_v(input('Введите x_1 начальнное'))
x[1, 0]=prov_v(input('Введите x_2 начальное'))


def graf(x):
    reng = np.mean([math.fabs(np.mean(x[0])), math.fabs(np.mean(x[1]))])
    Yy = np.arange(-1 * reng - 10, reng + 10, 0.1)
    Xx = np.arange(-1 * reng - 10, reng + 10, 0.1)
    X, Y = np.meshgrid(Xx, Yy)
    pylab.figure(1)
    cs = pylab.contour(X, Y, f(X, Y))
    pylab.clabel(cs, colors="black", fmt='x=%.2f')
    pylab.plot(x[0], x[1],'-g')
    pylab.plot(x[0], x[1], '*r')
    pylab.grid()
    pylab.show()
'''
# частная производная по х в виде выражения
def g_x_1():
     x_1, x_2 = sympy.symbols('x_1 x_2')
     return (sympy.diff(f(x_1, x_2), x_1))

# частная производная по у в виде выражения
def g_x_2():
    x_1, x_2 = sympy.symbols('x_1 x_2')
    return (sympy.diff(f(x_1, x_2), x_2))
'''
# частная производная по х_1 фннкции в принятой точке
def G_x_1(x1, x2):
    x_1, x_2 = sympy.symbols('x_1 x_2')
    return (sympy.diff(f(x_1, x_2), x_1).subs({x_1: x1, x_2: x2}))

# тоже частная производная по х_2 фннкции в принятой точке
def G_x_2(x1, x2):
    x_1, x_2 = sympy.symbols('x_1 x_2')
    return (sympy.diff(f(x_1, x_2), x_2).subs({x_1: x1, x_2: x2}))


#градиент твоей функции
def grad(x1,x2):
    x_1, x_2 = sympy.symbols('x_1 x_2')
    A = float(sympy.diff(sympy.diff(f(x_1,x_2),x_1), x_1).subs({x_1:x1, x_2:x2}))
    B = float(sympy.diff(sympy.diff(f(x_1,x_2),x_2), x_2).subs({x_1:x1, x_2:x2}))
    C = float(sympy.diff(sympy.diff(f(x_1,x_2),x_1), x_2).subs({x_1:x1, x_2:x2}))
    return (np.matrix([[A, C],
                       [C, B]]))

vector = lambda x_1, x_2: np.matrix([[G_x_1(x_1, x_2)],
                                    [G_x_2(x_1, x_2)]])



def Newton(x):
    x = np.hstack((x, np.matrix([[0], [0]])))
    x[:,1]=x[:,0]-np.dot(grad(x[0, 0], x[1, 0]).I, vector(x[0, 0], x[1, 0]))
    '''x[:,1]- воторой столбец матрицы х
       grad(x[0, 0], x[1, 0]).I - обратный градиент,  
       vector(x[0, 0], x[1, 0]) - вектор направлений найденый из частных производных
       np.dot(а,б) - перемножает матрицы а и б (а*б)'''
    return x
x= Newton(x)

print("х_1 =", x[0, 1],", х_2 =", x[1, 1], ". Минимум функции равен ",f(x[0,1],x[1,1]))
graf(x)