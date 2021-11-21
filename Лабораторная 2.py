import control
import numpy
import matplotlib.pyplot as plt
import sympy
import control.matlab as matlab
import math
#5.28129657228018

# Передаточные функции звеньев структурной схемы
oc = matlab.tf([5.281296400003636], [1])  # Отрицательная обратная связь
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
control.pzmap(d1, title='Карта полюсов и нулей замкнутой САУ')
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
control.pzmap(d2, title='Карта полюсов и нулей разомкнутой САУ')
plt.show()

# АФЧХ - годограф Найквиста
matlab.nyquist(d2)
plt.grid(True)
plt.title('АФЧХ - годограф Найквиста')
plt.xlabel('Re(s)')
plt.ylabel('Im(s)')
plt.show()

# 4. Снятие логарифмической амплитудной частотной и логарифмической фазовой частотной характеристик разомкнутой системы

matlab.bode(d2, omega_limits=[0.01, 1e5])
plt.show()

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

# 7. На основании алгебраического критерия Рауса–Гурвица
# рассчитать предельное значение Кос, при котором САУ теряет устойчивость

for k in numpy.arange(5.28, 5.3, 0.0000001):
    oc = matlab.tf([k], [1])
    d1 = matlab.feedback(d, oc)
    r1 = d1.den[0][0]
    dic1 = {}
    dlina1 = len(r1)
    for j in range(dlina1):
        dic1["%s" % j] = r1[j]
    matrix = numpy.array([[dic1["1"], dic1["3"]],
              [dic1["0"], dic1["2"]]])
    if (numpy.linalg.det(matrix) >= -0.0001) & (numpy.linalg.det(matrix) <= 0.0001):
        print('Предельное значение коэффициента обратной связи:', k)
        break






