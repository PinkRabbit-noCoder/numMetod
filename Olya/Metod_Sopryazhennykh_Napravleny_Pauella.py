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

print('Функция имеет вид : (x_1 - a)**2 +(x_2 - b)**2 + c*_1*x_2')
a = prov_v(input('Введите коэффициент a '))
b = prov_v(input('Введите коэффициент b '))
c = prov_v(input('Введите коэффициент c '))
f = lambda x_1, x_2: ((x_1 - a)**2) + ((x_2 - b)**2) + c*x_1*x_2# собственно твоя функция
x= np.empty([2,1])#массив с найденными точками
x[0, 0]=prov_v(input('Введите x_1 начальнное'))
x[1, 0]=prov_v(input('Введите x_2 начальное'))

def alpha(x_1,x_2,s):#функция находит альфу
    alpha = sympy.symbols('alpha')# обявление симвоольной переменной
    A = sympy.diff(f(x_1+alpha*s[0, 0], x_2+alpha*s[1, 0]), alpha)#находим производную от функции по альфа
    alpha = sympy.symbols('alpha')
    print(f(x_1+alpha*s[0, 0], x_2+alpha*s[1, 0]),'\n',A)#Выводим на экран функцию и производную
    for a in sympy.solve(A, alpha):#решение уравнения "производная = 0", функция возвращает массив корней
        alpha = float(a)# приводим к нормальному численому типу
    return alpha


s = np.matrix([[1, 0], # матрица векторов - направлений по осям
               [0, 1]])
n= 2 # порядак функции( максимальная степень агрумента - х и у)
al= []
i=0
while i <n**2-1:#необходимо провезти  n**2 одномерных поисков, -1 потому что в последнем поиска меняется направление
    print("Step ",i,'\n',x[:-1,])
    al.append(alpha(x[0, -1], x[1, -1], s[:, i%2]))#находим альфа
    print(al,'\n', x[:,-1]+np.dot(al[i], s[:, i % 2]))
    x=np.hstack((x,x[:, -1] + np.dot(al[i], s[:, i % 2])))#добовляем столбик к  маткрице х, в котором содержится новые ночки
    i=i+1
m=x.shape[1]
s = np.hstack((s,x[:,m-1]-x[:,1]))# к матрице направлений добавляем навый столбик, со значением равными раздницей между первой и последей точками,найдеными раниее
al.append(alpha(x[0, m-1], x[1, m-1], s[:,-1]))#находим последнюю альфу
x = np.hstack((x,x[:,m-1]+al[-1]*s[:,-1]))#находим последние точки
print(x)# выводим ррезультат
graf(x)#и строим график
