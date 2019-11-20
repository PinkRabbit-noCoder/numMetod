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

def graf(x):
    reng = np.mean([math.fabs(np.mean(x[0])), math.fabs(np.mean(x[1]))])
    Yy = np.arange(-1 * reng - 10, reng + 10, 0.1)
    Xx = np.arange(-1 * reng - 10, reng + 10, 0.1)
    X, Y = np.meshgrid(Xx, Yy)
    pylab.figure(1)
    cs = pylab.contour(X, Y, f(X, Y))
    pylab.clabel(cs, colors="black", fmt='x=%.2f')
    pylab.plot(x[0], x[1],'g-^')
    #pylab.plot(x[0], x[1], '*r')
    pylab.grid()
    pylab.show()

def G_x_1(x):
    x_1, x_2 = sympy.symbols('x_1 x_2')
    return (sympy.diff(f(x_1, x_2), x_1).subs({x_1: x[0,-1], x_2: x[1,-1]}))

# тоже частная производная по х_2 фннкции в принятой точке
def G_x_2(x):
    x_1, x_2 = sympy.symbols('x_1 x_2')
    return (sympy.diff(f(x_1, x_2), x_2).subs({x_1: x[0,-1], x_2: x[1,-1]}))

vector = lambda x: np.matrix([[G_x_1(x)],
                                    [G_x_2(x)]])
def alpha(x):
    alpha = sympy.symbols('alpha')
    A = sympy.diff(f(x[0,-1]+alpha*G_x_1(x), x[1,-1]+alpha*G_x_2(x)), alpha)
    print('\n',f(x[0,-1]+ alpha, x[1,-1] + alpha), '\n', A)   # выводит уравнение для альфа
    for a in sympy.solve(A, alpha):#решает уровенение и находит альфа
        alpha = float(a)
    print (" alpha = ", alpha)
    return alpha



x_i = lambda x, A: x[:,-1] + alpha(x)*A*vector(x)

print('Функция имеет вид : (x_1 - a)**2 +(x_2 - b)**2 + c*_1*x_2')
a = prov_v(input('Введите коэффициент a '))
b = prov_v(input('Введите коэффициент b '))
c = prov_v(input('Введите коэффициент c '))
f = lambda x_1, x_2: ((x_1 - a)**2) + ((x_2 - b)**2) + c*x_1*x_2# собственно твоя функция
x= np.empty([2,1])#массив с найденными точками
x[0, 0]=prov_v(input('Введите x_1 начальнное'))
x[1, 0]=prov_v(input('Введите x_2 начальное'))

#print(x[0, -1],x[1,-1],alpha(x),vector(x),alpha(x)*vector(x) ,x_i(x,1))

def kwNewton(x,e):
    i = 1
    A = []
    A.append(np.matrix([[1, 0],  # матрица векторов - направлений по осям
                        [0, 1]]))
    x = np.hstack((x, x_i(x,1)[:,-1]))
    while(np.abs(f(x[0,-2], x[1, -2])- f(x[0,-1],x[1,-1]))> e):
        delta_x = x[:,-1]- x[:,-2]
        delta_g = vector(x[:, -1])- vector(x[:, -2])
        print(vector(x[:, -2]), vector(x[:, -1]), x[:,-1])
        temp_1 = np.dot(delta_x , delta_x.transpose())/np.dot(delta_x.transpose(), delta_g)
        temp_2 = np.dot(np.dot(np.dot(A[i-1],delta_g) ,delta_g.transpose()),A[i-1])/np.dot(np.dot(delta_g.transpose(),A[i-1]),delta_g)
        Ac = A[i-1]+temp_1-temp_2
        print("\n дельта х\n",delta_x, "\n дельта g\n",delta_g, "\n A\n",Ac)
        A.append(Ac)
        x = np.hstack((x, x_i(x[:, -1], A[i])))
        i=i+1
    return x
print(kwNewton(x, 0.1))
graf(x)