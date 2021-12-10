import control
import numpy
import matplotlib.pyplot as plt
import sympy
import control.matlab as matlab
import math

kp = 39
kv = 1
tv = 0.3
kg = 2.8
tg = 5
ki = 4
# 0 Передаточная функция
w1 = matlab.tf([kp], [1])
print('w1 :', w1)
w2 = matlab.tf([kv], [tv, 1])
print('w2 :', w2)
w3 = matlab.tf([kg], [tg, 1])
print('w3 :', w3)
w4 = matlab.tf([ki], [1, 0])
print('w4 :', w4)
# Преобразование
w23 = w2 * w3 + 1
print('w23 :', w23)
w123 = w23 * w1
print('w123 :', w123)
w1234 = w123 + w4
f = w1234
print(f)
timeLine = []
for i in range(0, 10000):
    timeLine.append(i / 20)

plt.subplot(2, 1, 1)
plt.grid(True)
y, x = matlab.step(f, timeLine)
plt.plot(x, y, 'purple')
plt.title('Переходная характеристика')
plt.ylabel('Амплитуда')
plt.xlabel('Время (с)')
plt.show()
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
z = (dicu["0"]) * I * w ** 3 - (dicu["1"]) * w ** 2 + (dicu["2"]) * I * w
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

matrix = numpy.array([[dic1["1"], 0],
            [dic1["0"], dic1["2"]]])
print('Определитель n-1:', matrix)
# opred = dic1["1"] * dic1["2"] * dic1["3"] - dic1["1"] * dic1["4"] * dic1["1"] - dic1["3"] * dic1["0"] * dic1["3"]
# print('Определитель = ', dic1["1"], '*', dic1["2"], '*', dic1["3"], '-', dic1["1"], '*', dic1["4"], '*', dic1["1"], '-', dic1["3"], '*', dic1["0"], '*', dic1["3"], '=', opred)
print('Определитель n-1: равен = ', numpy.linalg.det(matrix))
if numpy.linalg.det(matrix) >= 0:
    print('2) Определитель n-1 положительный:', True)
else:
     print('2) Определитель n-1 положительный:', False)