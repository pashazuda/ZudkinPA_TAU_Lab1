import control
import numpy
import matplotlib.pyplot as plt
import sympy
import control.matlab as matlab
import math

# Передаточные функции звеньев структурной схемы
oc = matlab.tf([22], [1])  # Отрицательная обратная связь
gen = matlab.tf([1], [5, 1])  # Генератор
gturb = matlab.tf([0.02, 1], [0.25, 1])  # Гидравлическая турбина
isdev = matlab.tf([22], [20, 1])  # Исполнительное устройство

print('Отрицательная обратная связь: ', oc)
print('Генератор: ', gen)
print('Гидравлическая турбина: ', gturb)
print('Исполнительное устройство: ', isdev)

# Преобразование структурной схемы
d = gen*gturb*isdev  # Последовательное соединение динамических звеньев
print(d)
d1 = d/(1+d*oc)  # Для замкнутой системы
d2 = d*oc  # Для разомкнутой системы

# 1. Переходная характеристика
print('Передаточная функция замкнутой системы:')
print(d1)
timeLine = []
for i in range(0, 10000):
    timeLine.append(i / 1000)

plt.subplot(2, 1, 1)
plt.grid(True)
y, x = matlab.step(d1, timeLine)
plt.plot(x, y, 'purple')
plt.title('Переходная характеристика')
plt.ylabel('Амплитуда')
plt.xlabel('Время (с)')
plt.show()

# 2. Определение значения полюсов передаточной функции замкнутой САУ
a = matlab.pole(d1)
a = numpy.round(a, 2)
print('Полюса передаточной функции замкнутой САУ:')
print(a)

# Карта полюсов и нулей
control.pzmap(d1, title = 'Карта полюсов и нулей замкнутой САУ')
plt.show()

# 3. Оценка устойчивости по критерию Найквиста разомкнутой САУ
print('Передаточная функция разомкнутой системы:')
print(d2)

# Если разомкнутая система неустойчивая, то для определения устойчивости замкнутой системы
# необходиом найти число правых корней разомкнутой САУ
a = matlab.pole(d2)
a = numpy.round(a, 2)
print('Полюса передаточной функции разомкнутой САУ:')
print(a)

# Карта полюсов и нулей
control.pzmap(d2, title = 'Карта полюсов и нулей разомкнутой САУ')
plt.show()

# АФЧХ - годограф Найквиста
matlab.nyquist(d2)
plt.grid(True)
plt.title('АФЧХ - годограф Найквиста')
plt.xlabel('Re(s)')
plt.ylabel('Im(s)')
plt.show()

# 4. Снятие логарифмической амплитудной частотной и логарифмической фазовой частотной характеристик разомкнутой системы

matlab.bode(d2)
plt.show()

# 6. Построить годограф Михайлова. Сделать вывод об устойчивости САУ по критерию Михайлова
from sympy import *
from numpy import arange
import matplotlib.pyplot as plt
w =symbols(' w',real=True)
z=-625*w**6 + 5312*I*w**5 + (1.279e+04)*w**4 - (1.854e+04)*I*w**3 - (5.252e+04)*w**2 + (1.228e+04)*I*w + 485
z=-625*w**6 + 5312*I*w**5 + (1.279*10**(+4))*w**4 - (1.854*10**(+4))*I*w**3 - (5.252*10**(+4))*w**2 + (1.228*10**(+4))*I*w + 485
print("Характеристический многочлен замкнутой системы: %s"%z)
zr=re(z)
zm=im(z)
print("Начальная точка М(%s,%s)"%(zr.subs({w:0}),zm.subs({w:0})))
print("Действительная часть Re= %s"%zr)
print("Мнимая часть Im= %s"%zm)
x=[zr.subs({w:q}) for q in arange(0,100,0.1)]
y=[zm.subs({w:q}) for q in arange(0,100,0.1)]
plt.axis([-1000.0, 1000.0, -3000.0, 3000.0])
plt.plot(x, y)
plt.grid(True)
plt.show()
