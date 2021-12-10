import control
import numpy
import matplotlib.pyplot as plt
import sympy
import control.matlab as matlab
import math
kp = 0.55
ki = 0.027500000000004
kd = 0.935
# 5.28129657228018
# Передаточные функции звеньев структурной схемы
oc = matlab.tf([1], [1])  # Отрицательная обратная связь
gen = matlab.tf([1], [5, 1])  # Генератор
gturb = matlab.tf([0.02, 1], [0.25, 1])  # Гидравлическая турбина
isdev = matlab.tf([22], [20, 1])  # Исполнительное устройство
prop = matlab.tf([kp], [1])
int = matlab.tf([ki], [1, 0])
dif = matlab.tf([kd, 0], [1])

# Преобразование структурной схемы
pid = prop + int + dif
d = pid * gen * gturb * isdev  # Последовательное соединение динамических звеньев
d1 = matlab.feedback(d, oc)  # Для замкнутой системы
d2 = d * oc  # Для разомкнутой системы

# 1. Переходная характеристика


timeLine = []
for i in range(0, 10000):
    timeLine.append(i / 350)

plt.subplot(2, 1, 1)
plt.grid(True)
y, x = matlab.step(d1, timeLine)
plt.plot(x, y, 'purple')
plt.title('Переходная характеристика')
plt.ylabel('Амплитуда')
plt.xlabel('Время (с)')
plt.show()
# Удаление максимума
ind1 = numpy.argmax(y)
index1 = []
for i in range(0, ind1):
    index1.append(i)

y1 = numpy.delete(y, index1)
x1 = numpy.delete(x, index1)
# Удаоение до минимума2
ind2 = numpy.argmin(y1)
index2 = []
for i in range(0, ind2):
    index2.append(i)
y2 = numpy.delete(y1, index2)
x2 = numpy.delete(x1, index2)
# Удаоение до максимума2
ind3 = numpy.argmax(y2)
index3 = []
for i in range(0, ind3):
    index3.append(i)
y3 = numpy.delete(y2, index3)
x3 = numpy.delete(x2, index3)
# Первый максимум
a1 = max(y)
# Второй максимум
a2 = max(y2)
t = None
# Нахождение установившегося значения
for i in range(len(x3)):
    if x3[i] == 30:
        t = i
h_500 = y[t]
h_yst1 = h_500 + h_500 * 0.05
h_yst2 = h_500 + h_500 * 0.05
print(h_500, h_yst1)
# Нахождение времени установившегося значения
l1 = 0
for i in range(t):
    if (h_yst1 - 0.1 < y3[i] < h_yst1 + 0.1) or (h_yst2 - 0.1 < y3[i] < h_yst2 + 0.1):
        l1 = x3[i]
# Нахождение перерегулирования
per = ((a1 - h_500) / h_500) * 100
l2 = per
# Нахождение показателя колебательности
timeLine = []
for i in range(0, 300):
    timeLine.append(i / 300)

plt.subplot(2, 1, 1)
plt.grid(True)
mag, phase, omega = matlab.freqresp(d1, timeLine)
plt.plot(mag)
plt.title('АЧХ')
plt.ylabel('Амплитуда')
plt.xlabel('Угловая частота, (рад/с)')
a_max = max(mag)
a_0 = mag[0]
l3 = a_max / a_0
print('Кпроп:', kp)
print('Кинт:', ki)
print('Кдиф:', kd)
print('Время регулирования: 15 = ', l1)
print('Перерегулирование: 21 = ', l2)
print('Показатель колебательности: 1.16 = ', l3)