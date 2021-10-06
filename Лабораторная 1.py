import numpy
import matplotlib.pyplot as plt
import sympy
import control.matlab as matlab
import math


def choice():
    bezinerc = 'Безинерционное звено'
    aperiod = 'Апериодическое звено'
    integrir = 'Интегрирующее звено'
    idealdif = 'Идеальное дифференцирующее звено'
    realdif = 'Реальное дифференцирующее звено'

    needNewChoice = True
    while needNewChoice:
        userInput = input('Введите номер команды:\n'
                          '1 - Безинерционное звено;\n'
                          '2 - Апериодическое звено;\n'
                          '3 - Интегрирующее звено;\n'
                          '4 - Идеальное дифференцирующее звено;\n'
                          '5 - Реальное дифференцирующее звено;\n')

        if userInput.isdigit():
            needNewChoice = False
            userInput = int(userInput)
            if userInput == 1:
                name = bezinerc
            elif userInput == 2:
                name = aperiod
            elif userInput == 3:
                name = integrir
            elif userInput == 4:
                name = idealdif
            elif userInput == 5:
                name = realdif
            else:
                print('\n Пожалуйста введите числовое значение от 1 до 5')
                needNewChoice = True

        else:
            print('\n Пожалуйста введите числовое значение')
            needNewChoice = True
    return name


def getUnit(name):
    needNewChoice = True
    while needNewChoice:

        k = input('Пожалуйста введите кэффициент "k", если его значение не дано введите "0":')
        t = input('Пожалуйста введите кэффициент "t", если его значение не дано введите "0":')

        def is_number(str):
            try:
                float(str)
                return True
            except ValueError:
                return False

        if is_number(k) and is_number(t):
            needNewChoice = False
            k = float(k)
            t = float(t)
            if k != 0 and t != 0:
                if name == 'Апериодическое звено':
                    unit = matlab.tf([k], [t, 1])
                elif name == 'Реальное дифференцирующее звено':
                    unit = matlab.tf([k, 0], [t, 1])
                # Для случая если человек выбрал безинерционное звено и веел данные для k и t
                elif name == 'Безинерционное звено':
                    print('\nДля безиннерционного звена t не может быть задан, пожалуйста повторите ввод')
                    return getUnit(name)
                # Для случая если человек выбрал интегрирующее звено и веел данные для k и t
                elif name == 'Интегрирующее звено':
                    print('\nДля интегрирующего звена может быть задан только один из коэффициентов, пожалуйста '
                          'повторите ввод')
                    return getUnit(name)
                # Для случая если человек выбрал идеальное дифференцирующее звено и веел данные для k и t
                elif name == 'Идеальное дифференцирующее звено':
                    print('\nДля идеального дифференцирующего звена может быть задан только один из коэффициентов, '
                          'пожалуйста повторите ввод')
                    return getUnit(name)
            # Для ваирианта когда k не задано, а t задано
            elif k == 0 and t != 0:
                if name == 'Интегрирующее звено':
                    unit = matlab.tf([1], [t, 0])
                elif name == 'Идеальное дифференцирующее звено':
                    unit = matlab.tf([t, 0], [0.0000000000000000000001, 1])
                # Для случая если человек выбрал безинерционное звено и не веел данные для k
                elif name == 'Безинерционное звено':
                    print('\nДля безиннерционного звена k не может быть не задана, пожалуйста повторите ввод')
                    return getUnit(name)
            # Для ваирианта когда k задано, а t не задано
            elif k != 0 and t == 0:
                if name == 'Безинерционное звено':
                    unit = matlab.tf([k], [1])
                elif name == 'Интегрирующее звено':
                    unit = matlab.tf([k], [1, 0])
                elif name == 'Идеальное дифференцирующее звено':
                    unit = matlab.tf([k, 0], [0.0000000000000000000001, 1])
            # Если для обоих коэффициентов ввели 0 по ошибке
            elif k == 0 and t == 0:
                print('\nОба коэффициента не могут быть не заданы, пожалуйста повторите ввод')
                return getUnit(name)
        else:
            print('\nПожалуйста введите числовое значение')
            needNewChoice = True
    return unit


def graph(num, title, y, x):
    plt.subplot(2, 2, num)
    plt.grid(True)
    if title == 'Переходная характеристика':
        plt.plot(x, y, 'purple')
    elif title == 'Импульсная характеристика':
        plt.plot(x, y, 'green')
    plt.title(title)
    plt.ylabel('Амплитуда')
    plt.xlabel('Время (с)')


zvenoName = choice()
peredFunc = getUnit(zvenoName)
print(zvenoName)
print(peredFunc)

timeLine = []
for i in range(0, 10000):
    timeLine.append(i / 1000)

[y, x] = matlab.step(peredFunc, timeLine)
graph(1, 'Переходная характеристика', y, x)
[y, x] = matlab.impulse(peredFunc, timeLine)
graph(2, 'Импульсная характеристика', y, x)



plt.subplot(2,2,3)
plt.grid(True)
mag, phase, omega = matlab.freqresp(peredFunc, timeLine)
plt.plot(mag)
plt.title('АЧХ')
plt.ylabel('Амплитуда')
plt.xlabel('Угловая частота, (рад/с)')

plt.subplot(2,2,4)
plt.grid(True)
plt.plot(phase*180/math.pi)
plt.title('ФЧХ')
plt.ylabel('Фаза')
plt.xlabel('Угловая частота, (рад/с)')
plt.show()

