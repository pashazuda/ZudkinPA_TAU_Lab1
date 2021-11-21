import control
import numpy
import matplotlib.pyplot as plt
import sympy
import control.matlab as matlab
import math
#5.281294901069271
#5.2812949002279765
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
d = gen * gturb * isdev  # Последовательное соединение динамических звеньев
d1 = matlab.feedback(d, oc)  # Для замкнутой системы
d2 = d * oc  # Для разомкнутой системы

# 1. Переходная характеристика
print('Передаточная функция замкнутой системы:')
print(d1)

# 6. Построить годограф Михайлова. Сделать вывод об устойчивости САУ по критерию Михайлова

from sympy import *
from numpy import arange
import matplotlib.pyplot as plt
u = d1.den[0][0]
dicu = {}
dlinau = len(u)
for i in range(dlinau):
        dicu["%s" % i] = u[i]
w = symbols(' w', real=True)
z = -(dicu["0"]) * I * w ** 3 - (dicu["1"]) * w ** 2 + (dicu["2"]) * I * w + (dicu["3"])
# z = -25 * I * w ** 3 - 106.2 * w ** 2 + 34.93 * I * w + 485 для k = 22
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
