import control
import numpy
import matplotlib.pyplot as plt
import sympy
import control.matlab as matlab
import math
import scipy
def regul(name):
    if name == 'ПИД':
        kp = 1.01
        ki = 0.019
        kd = 1.1405
        prop = matlab.tf([kp], [1])
        int = matlab.tf([ki], [1, 0])
        dif = matlab.tf([kd, 0], [1])
        pid = control.parallel(prop, int, dif)
        return pid
    elif name == 'П':
        kp = 0.23
        prop = matlab.tf([kp], [1])
        return prop


name_regul = input('Введите наименование регулятора (ПИД или П):')
# Передаточные функции звеньев структурной схемы
oc = matlab.tf([1], [1])  # Отрицательная обратная связь
gen = matlab.tf([1], [5, 1])  # Генератор
gturb = matlab.tf([0.02, 1], [0.25, 1])  # Гидравлическая турбина
isdev = matlab.tf([22], [20, 1])  # Исполнительное устройство


# Преобразование структурной схемы

d = control.series(regul(name_regul), gen, gturb, isdev)
d1 = matlab.feedback(d, oc)  # Для замкнутой системы
print(d1)
# 3. Прямы оценки качества регулирования
# 1. Переходная характеристика
timeLine = numpy.arange(0, 100.01, 0.1)
plt.subplot(1, 1, 1)
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
t_infinity = 100
t = None
# Нахождение установившегося значения
for i in range(len(x1)-1):
    if x1[i] <= t_infinity:
        t = i
h_infinity = y1[t]
h_yst1 = h_infinity * 1.05
h_yst2 = h_infinity * 0.95
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
colebat_3 = a1_3 / a2_3
# Нахождение перерегулирования
per_3 = ((a1_3 - h_infinity) / h_infinity) * 100
# Вывод дзначений для пункта 3
print('2. Прямые оценки качества переходного процесса')
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
plt.hlines(1.05 * y[len(timeLine) - 1], 0, 100)
plt.hlines(0.95 * y[len(timeLine) - 1], 0, 100)
plt.show()

# 4. По распределению корней на комплексной плоскости замкнутой САУ
# Определение значения полюсов передаточной функции замкнутой САУ
a = matlab.pole(d1)
a = numpy.round(a, 3)
print('Полюса передаточной функции замкнутой САУ:')
print(a)
znach = -1000
for i in range(len(a)-2):
 if a[i].real >= znach:
    znach = a[i].real
t_reg_4 =math.fabs(3 / znach)  # Время регулирования
# Определение максимальной степени колебательности
max4 = 0
colebat_4 = 0
for i in a:
    colebat_4 = math.fabs(sympy.im(i) / sympy.re(i))
    if colebat_4 > max4:
        max4 = colebat_4
colebat_4 = max4
# Определение перерегулирования
per_4 = math.e**(-math.pi / colebat_4)
# Опеределение колебательности
stepen_zatuh_4 = 1 - math.e**(-2 * math.pi / colebat_4)
# Карта полюсов и нулей
control.pzmap(d1, title='Карта полюсов и нулей замкнутой САУ')
plt.show()
# Вывод дзначений для пункта 4
print('3. По распределению корней на комплексной плоскости замкнутой САУ')
print('а) Время регулирования:', t_reg_4)
print('б) Перерегулирование:', per_4)
print('в) Колебательность:', colebat_4)
print('г) Степень затухания:', stepen_zatuh_4)
# 5. По логарифмическим частотным характеристикам:
# Нахождение показателя колебательности
timeLine = numpy.arange(0, 5, 0.1)
plt.subplot(1, 1, 1)
plt.grid(True)
mag, phase, omega = matlab.freqresp(d1, timeLine)
a_max = max(mag)
a_0 = mag[0]
ind_mag_max = numpy.argmax(mag)
#Удаление значений до максимума
index_mag = []
for i in range(0, ind_mag_max):
    index_mag.append(i)
mag1 = numpy.delete(mag, index_mag)
omega1 = numpy.delete(omega, index_mag)
id_omega_srez = 0
for i in range(len(mag1) - 1):
    if mag1[i] >= mag[0] >= mag1[i + 1]:
        id_omega_srez = i
omega_sreza = omega1[id_omega_srez]
t_reg_5 = 1 * ((2 * math.pi) / omega_sreza)
plt.plot(omega, mag, 'purple')
plt.title('АЧХ')
plt.ylabel('Амплитуда')
plt.xlabel('Угловая частота, (рад/с)')
plt.hlines(mag[0], 0, 3, linestyles='--')
plt.show()
pokaz_koleb_5 = a_max / a_0
# Вывод дзначений для пункта 4
print('4. По логарифмическим частотным характеристикам')
print('а) Время регулирования:', t_reg_5)
print('б) Показатель колебательности:', pokaz_koleb_5)
mag, phase, omega = matlab.bode(d1)
plt.show()
# 6. По интегральному методу:
from scipy import integrate
timeLine = numpy.arange(0, 100.01, 0.1)
y, x = matlab.step(d1, timeLine)
y_integr = []
for i in y:
    y_integr.append(math.fabs(h_infinity - i))
Q = integrate.trapezoid(y_integr, x)
print('5. По интегральному методу')
print('Интеграл равен', Q)
print()
print('Показатели качества')
print('Время регулирования: 15 = ', t_reg_3)
print('Перерегулирование: 21 = ', per_3)
print('Показатель колебательности: 1.16 = ', pokaz_koleb_5)




