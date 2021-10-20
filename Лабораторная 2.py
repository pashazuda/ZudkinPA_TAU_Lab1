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

print(oc)
print(gen)
print(gturb)
print(isdev)

# Преобразование структурной схемы
d = gen*gturb*isdev  # Последовательное соединение динамических звеньев
d1 = d/(1+d*oc)  # Для замкнутой системы
d2 = d*oc  # Для разомкнутой системы

# 1. Переходная характеристика
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
print(a)
s = sympy.symbols('s')
expr = 625*(s**6) + 5312*(s**5) + (1.279e+04)*(s**4) + (1.854e+04)*(s**3) + (5.252e+04)*(s**2) + (1.228e+04)*s + 485
f = sympy.solve(sympy.Eq(expr, s))
print(f)

# Карта полюсов и нулей
control.pzmap(d1, title = 'Карта полюсов и нулей')
plt.show()