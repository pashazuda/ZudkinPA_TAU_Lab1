import control
import numpy
import matplotlib.pyplot as plt
import sympy
import control.matlab as matlab
import math

name_regul = 'ПИД'
# 5.28129657228018
# Передаточные функции звеньев структурной схемы
for kp in numpy.arange(0.2, 200, 0.01):
            oc = matlab.tf([1], [1])  # Отрицательная обратная связь
            gen = matlab.tf([1], [5, 1])  # Генератор
            gturb = matlab.tf([0.02, 1], [0.25, 1])  # Гидравлическая турбина
            isdev = matlab.tf([22], [20, 1])  # Исполнительное устройство
            prop = matlab.tf([kp], [1])


            # Преобразование структурной схемы
            d = control.series(prop, gen, gturb, isdev)  # Последовательное соединение динамических звеньев
            d1 = matlab.feedback(d, oc)  # Для замкнутой системы

            # 3. Прямы оценки качества регулирования
            # 1. Переходная характеристика
            timeLine = numpy.arange(0, 100, 0.1)
            plt.subplot(3, 1, 1)
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
            colebat_3 = 0
            if name_regul == 'ПИД':
                colebat_3 = 1
            # Нахождение перерегулирования
            per_3 = ((a1_3 - h_infinity) / h_infinity) * 100


            # 4. По распределению корней на комплексной плоскости замкнутой САУ
            # Определение значения полюсов передаточной функции замкнутой САУ
            a = matlab.pole(d1)
            a = numpy.round(a, 3)

            # Карта полюсов и нулей
            control.pzmap(d1, title='Карта полюсов и нулей замкнутой САУ')

            # 5. По логарифмическим частотным характеристикам:
            # Нахождение показателя колебательности
            timeLine = numpy.arange(0, 5, 0.1)
            plt.subplot(3, 1, 2)
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
                # print(mag1[i], mag[0])
                if mag1[i] >= mag[0] >= mag1[i + 1]:
                    id_omega_srez = i
            omega_sreza = omega1[id_omega_srez]

            t_reg_5 = 1 * ((2 * math.pi) / omega_sreza)
            plt.plot(omega, mag, 'purple')
            plt.title('АЧХ')
            plt.ylabel('Амплитуда')
            plt.xlabel('Угловая частота, (рад/с)')
            plt.hlines(mag[0], 0, 3)

            pokaz_koleb_5 = a_max / a_0
            if (t_reg_3 in numpy.arange(14.5, 15.5, 0.001)) and (per_3 in numpy.arange(20, 22, 0.001)) and (pokaz_koleb_5 in numpy.arange(1.1, 1.3, 0.001)):
                print('Кпроп:', kp)
                print('Время регулирования: 15 = ', t_reg_3)
                print('Перерегулирование: 21 = ', per_3)
                print('Показатель колебательности: 1.16 = ', pokaz_koleb_5)


