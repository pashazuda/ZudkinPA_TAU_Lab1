import control
import numpy
import matplotlib.pyplot as plt
import sympy
import control.matlab as matlab
import math
# 0 Передаточная функция
f = matlab.tf([189, 63], [19.2, 57.4, 43.7, 11.9, 7.3])
print(f)
# 1.1 Годограф михайлова
print('1.1 Годограф михайлова')
from sympy import *
from numpy import arange
import matplotlib.pyplot as plt
u = f.den[0][0]
dicu = {}
dlinau = len(u)
for i in range(dlinau):
        dicu["%s" % i] = u[i]
print('Знаменатель: ', dicu)
w = symbols(' w', real=True)
z = (dicu["0"]) * w ** 4-(dicu["1"]) * I * w ** 3 - (dicu["2"]) * w ** 2 + (dicu["3"]) * I * w + (dicu["4"])
print(z)
print("Характеристический многочлен замкнутой системы: %s" % z)
zr = re(z)
zm = im(z)
print("Начальная точка М(%s,%s)" % (zr.subs({w: 0}), zm.subs({w: 0})))
print("Действительная часть Re= %s" % zr)
print("Мнимая часть Im= %s" % zm)
x = [zr.subs({w: q}) for q in arange(0, 100, 0.1)]
y = [zm.subs({w: q}) for q in arange(0, 100, 0.1)]
plt.axis([-100000.0, 100000.0, -300000.0, 300000.0])
plt.title("Начальная точка М(%s,%s)" % (zr.subs({w: 0}), zm.subs({w: 0})))
plt.plot(x, y)
plt.grid(True)
plt.show()
# 1.2 Критерий Гурвица
print('1.2 Критерий Гурвица')
r1 = f.den[0][0]
dic1 = {}
dlina1 = len(r1)
logic12 = False
for j in range(dlina1):
    dic1["%s" % j] = r1[j]
    print("a%s" % j,'=', r1[j])
    if r1[j] >= 0:
        logic12 = True
    else:
        logic12 = False
print('1) Все коэффициенты положительные:', logic12)

matrix = numpy.array([[dic1["1"], dic1["3"], 0],
            [dic1["0"], dic1["2"], dic1["4"]],
            [0, dic1["1"], dic1["3"]]])
print('Определитель n-1:', matrix)
opred = dic1["1"] * dic1["2"] * dic1["3"] - dic1["1"] * dic1["4"] * dic1["1"] - dic1["3"] * dic1["0"] * dic1["3"]
print('Определитель = ', dic1["1"], '*', dic1["2"], '*', dic1["3"], '-', dic1["1"], '*', dic1["4"], '*', dic1["1"], '-', dic1["3"], '*', dic1["0"], '*', dic1["3"], '=', opred)
print('Определитель n-1: равен = ', numpy.linalg.det(matrix))
if numpy.linalg.det(matrix) >= 0:
    print('2) Определитель n-1 положительный:', True)
else:
     print('2) Определитель n-1 положительный:', False)

# 2 Aнализ качества переходного процесса
print('2 Aнализ качества переходного процесса')
# 2.1 По переходной характеристике
print('Передаточная функция замкнутой системы:')
timeLine = []
for i in range(0, 10000):
    timeLine.append(i / 20)
plt.subplot(1, 1, 1)
plt.grid(True)
y, x = matlab.step(f, timeLine)
plt.plot(x, y, 'purple')
plt.title('Переходная характеристика')
plt.ylabel('Амплитуда')
plt.xlabel('Время (с)')
plt.show()

# 2.1.1 Время регулирования
print('2.1.1 Время регулироваия')
h_yst = float(input('Введите установившееся значение:'))
h_reg = h_yst + h_yst * 0.05
print('h для нахождения времени регулирования:', h_reg)
# t_reg = 190c

# 2.1.2 Перерегулирование
print('2.1.2 Перерегулирование')
h_max = float(input('Введите максимальное значение А1:'))
preg = ((h_max - h_yst) / h_yst) * 100
print('Перерегулирование:', preg)
# 2.1.3 Колебательность
print('2.1.3 Колебательность')
t_reg = float(input('Введите время регулирования:'))
tk = float(input('Введите Tk:'))
print('Колебательность:', t_reg/tk)
# 2.1.4 Степень затухания
print('2.1.4 Степень затухания')
h_max2 = float(input('Введите значение А2:'))
print('Степень затухания:', (h_max - h_max2) / (h_max - h_yst))

# 2.2 По распределению корней и полюсов на комплексной плоскости
print('2.2 По распределению корней и полюсов на комплексной плоскости')
# Полюса и нули
a = matlab.pole(f)
a = numpy.round(a, 2)
print('Полюса передаточной функции замкнутой САУ:')
print(a)
# Карта полюсов и нулей
control.pzmap(f, title='Карта полюсов и нулей замкнутой САУ')
plt.show()
# 2.2.1 Время регулирования
pole_min = float(input('Введите значение min|ReЛi|:'))
print('Время регулирования:', 3/pole_min)
# 2.2.2 Степень колебательности
pole_max_a = float(input('Введите значение Альфа пары комплексных корней:'))
pole_max_b = float(input('Введите значение Бетта пары комплексных корней:'))
s_kol = pole_max_b / pole_max_a
print('Степень колебательности:', s_kol)
# 2.2.3 Перерегулирование
print('Перерегулирование:', (math.exp((-math.pi)/s_kol))*100)

# 2.3. По критерию Найквиста определить
print('2.3. По критерию Найквиста определить:')
phase_a = float(input('Введите значение Альфа фазы:'))
phase_b = float(input('Введите значение Бетта фазы:'))
z_phase = math.atan(phase_b / phase_a) * (180 / math.pi)
print('Запас по фазе:', z_phase)
h_a = float(input('Введите значение |Альфа| при Бетта=0:'))
print('Запас по амплитуде:', 1 - h_a)

# 2.4. По АЧХ определить
print('2.4. По АЧХ определить:')
a0 = float(input('Введите значение А0:'))
amax = float(input('Введите значение Аmax:'))
print('Показатель колебательности:', amax / a0)
phase1 = float(input('Введите значениt частоты среза:'))
print('Время регулирования:', 1.5*(2*math.pi/phase1))

