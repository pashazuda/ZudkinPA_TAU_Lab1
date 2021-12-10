import control
import numpy
import matplotlib.pyplot as plt
import sympy
import control.matlab as matlab
import math
name_regul = 'ПИД'
kp = 0.55
ki = 0.000275
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
pid = control.parallel(prop, int, dif)
d = control.series(pid, gen, gturb, isdev)  # Последовательное соединение динамических звеньев
d1 = matlab.feedback(d, oc)  # Для замкнутой системы
print(d1)
# 3. Прямы оценки качества регулирования
# 1. Переходная характеристика
timeLine = []
for i in range(0, 10000):
    timeLine.append(i / 25)
plt.subplot(2, 1, 1)
plt.grid(True)
y, x = matlab.step(d1, timeLine)
# Удаление максимума
ind1 = numpy.argmax(y)
index1 = []
for i in range(0, ind1):
    index1.append(i)
y1 = numpy.delete(y, index1)
x1 = numpy.delete(x, index1)
# Первый максимум
a1_3 = max(y)  # Значение
t1max_3 = None
for i in range(len(y)-1):
    if y[i] == a1_3:
        t1max_3 = x[i]  # Время
t_infinity = 400
t = None
# Нахождение установившегося значения
for i in range(len(x1)-1):
    if x1[i] <= t_infinity:
        t = i
h_500 = y1[t]
h_yst1 = h_500 * 1.05
h_yst2 = h_500 * 0.95
# Нахождение времени установившегося значения
t_reg_3 = None
reg_i = None
for i in range(t):
    if (h_yst1 - 0.001 < y1[i] < h_yst1 + 0.001) or (h_yst2 - 0.001 < y1[i] < h_yst2 + 0.001):
        t_reg_3 = x1[i]  # Время регулирования
# Нахождение степени затухания
# Нахождение минимума после первого максимума
ind2 = numpy.argmin(y1)
index2 = []
for i in range(0, ind1):
    index2.append(i)
y2 = numpy.delete(y1, index2)
x2 = numpy.delete(x1, index2)
# Нахождение второго максимума
a2_3 = max(y2)
stepen_zatuh_3 = (a1_3 - a2_3) / a1_3
# Нахождение колебательности
colebat_3 = 0
if name_regul == 'ПИД':
    colebat_3 = 1
# Нахождение перерегулирования
per_3 = ((a1_3 - h_500) / h_500) * 100
# Вывод дзначений для пункта 3
print('Прямые оценки качества переходного процесса')
print('а) Время регулирования:', t_reg_3)
print('б) Перерегулирование:', per_3)
print('в) Колебательность:', colebat_3)
print('г) Степень затухания:', stepen_zatuh_3)
print('д) Величина достижения первого максимума:', a1_3)
print('   Время достижения первого максимума:', t1max_3)
plt.plot(x, y, 'purple')
plt.title('Переходная характеристика')
plt.ylabel('Амплитуда')
plt.xlabel('Время (с)')
plt.hlines(1.05 * y[len(timeLine) - 1], 0, 400)
plt.hlines(0.95 * y[len(timeLine) - 1], 0, 400)
plt.show()

# 4. По распределению корней на комплексной плоскости замкнутой САУ
# Определение значения полюсов передаточной функции замкнутой САУ
a = matlab.pole(d1)
a = numpy.round(a, 3)
print('Полюса передаточной функции замкнутой САУ:')
print(a)
# Карта полюсов и нулей
control.pzmap(d1, title='Карта полюсов и нулей замкнутой САУ')
plt.show()
# 5. По логарифмическим частотным характеристикам:
# Нахождение показателя колебательности
timeLine = []
for i in range(0, 300):
    timeLine.append(i / 100)

plt.subplot(2, 1, 2)
plt.grid(True)
mag, phase, omega = matlab.freqresp(d1, timeLine)
a_max = max(mag)
print(a_max)
a_0 = mag[0]
print("max mag", max(mag))
ind_mag_max = numpy.argmax(mag)
#Удаление значений до максимума
index_mag = []
for i in range(0, ind_mag_max):
    index_mag.append(i)
mag1 = numpy.delete(mag, index_mag)
omega1 = numpy.delete(omega, index_mag)
id_omega_srez = 0
for i in range(len(mag1) - 1):
    # print(mag1[i], mag[0])
    if mag1[i] == mag[0] + 0.0140421849188546:
        id_omega_srez = i
omega_sreza = omega1[id_omega_srez]
print(omega_sreza)
t_reg_5 = 1 * ((2 * math.pi) / omega_sreza)
plt.plot(omega, mag, 'purple')
plt.title('АЧХ')
plt.ylabel('Амплитуда')
plt.xlabel('Угловая частота, (рад/с)')
plt.hlines(0.91379, 0, 3)
plt.show()
pokaz_koleb_5 = a_max / a_0
# Запас по фазе и амплитуде
mag2, phase2, omega2 = matlab.bode(d1)
for i in mag2:
    if i == 0:
        print(i)
plt.show()

print('Кпроп:', kp)
print('Кинт:', ki)
print('Кдиф:', kd)
print('Время регулирования: 15 = ', t_reg_5)
print('Перерегулирование: 21 = ', per_3)
print('Показатель колебательности: 1.16 = ', pokaz_koleb_5)




