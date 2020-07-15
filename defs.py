from math import pi

"""Добавил"""
def interpolation(y_max, y_min, x_max, x_min, x):
    """Функция проводит интерполяцию данных"""
    return (y_max - y_min) / (x_max - x_min) * (x - x_min) + y_min


def w_count(G, d, ro):
    """Функция считает скорость по уравнению неразрывности"""
    return G / (ro * pi * d ** 2 / 4)


def Re_count(w, d, ny):
    """Функция считает число Рейнольдса"""
    return w * d / ny


def Pr_count(c, ro, ny, lyambda):
    """Функция считает число Прандтля"""
    return c * ro * ny / lyambda


def et_count(Pr_water, Pr_wall):
    """Функция считает попровку на температуру"""
    return (Pr_water / Pr_wall) ** 0.25


def el_lam_count(l, d):
    """Функция считает поправку на участок стабилизации при ламинарном режиме"""
    el_m = [[1, 1.9], [4, 1.7], [5, 1.44], [10, 1.28], [15, 1.18], [20, 1.13], [30, 1.05], [40, 1.02], [50, 1]]
    if l / d >= 50:
        return 1
    elif l / d < 1:
        print('Диаметр превышает значение длины трубы!')
    else:
        for i in el_m:
            if i[0] == l / d:
                return i[1]
            else:  # Если такого отношения нет, то делается интерполяция по вышеуказанной функции interpolation
                for j in range(len(el_m)):
                    if el_m[j + 1][0] > l / d > el_m[j][0]:
                        return interpolation(el_m[j + 1][1], el_m[j][1], el_m[j + 1][0], el_m[j][0], l / d)


def el_turb_count(Re, l, d):
    """Функция считает поправку на участок стабилизации при турбулентном режиме"""
    el_m = [[0, 1, 2, 5, 10, 15, 20, 30, 40, 50],
                 [10000, 1.65, 1.50, 1.34, 1.23, 1.17, 1.13, 1.07, 1.03, 1],
                 [20000, 1.51, 1.4, 1.27, 1.18, 1.13, 1.1, 1.05, 1.02, 1],
                 [50000, 1.34, 1.27, 1.18, 1.13, 1.1, 1.08, 1.04, 1.02, 1],
                 [100000, 1.28, 1.22, 1.15, 1.1, 1.08, 1.06, 1.03, 1.02, 1],
                 [1000000, 1.14, 1.11, 1.08, 1.05, 1.04, 1.03, 1.02, 1.01, 1]]
    if not 10000 <= Re <= 1000000:
        print('Режим не турбулентный!')
    else:
        for i in range(len(el_m)):
            if Re == el_m[i][0]:
                for j in range(0, len(el_m[0])):
                    if l / d == el_m[0][j]:
                        return el_m[i][j]
                    elif el_m[0][j] > l / d > el_m[0][j - 1]:
                        return interpolation(el_m[i][j], el_m[i][j - 1], el_m[0][j], el_m[0][j - 1], l / d)
            elif el_m[i][0] > Re > el_m[i - 1][0]:
                for j in range(0, len(el_m[0])):
                    if l / d == el_m[0][j]:
                        return interpolation(el_m[i][j], el_m[i - 1][j], el_m[i][0], el_m[i - 1][0], Re)
                    elif el_m[0][j] > l / d > el_m[0][j - 1]:
                        inter_min = interpolation(el_m[i - 1][j], el_m[i - 1][j - 1], el_m[0][j], el_m[0][j - 1], l / d)
                        inter_max = interpolation(el_m[i][j], el_m[i][j - 1], el_m[0][j], el_m[0][j - 1], l / d)
                        return interpolation(inter_max, inter_min, el_m[i][0], el_m[i - 1][0], Re)


def Nu_lam_count(Re, Pr, et, el):
    """Функция считает число Нуссельта при ламинарном движении (автор Михеев М. А.)"""
    return 0.15 * (Re ** 0.33) * (Pr ** 0.43) * et * el


def Nu_per_count(Re, Pr, et):
    """Функция производит расчет числа Нуссельта для переходного режима (автор Михеев М.А.)"""
    k_miheev = [[2.1, 1.9], [2.2, 2.2], [2.3, 3.3], [2.4, 3.8], [2.5, 4.4], [3.0, 6.0], [4.0, 10.3], [5.0, 15.5],
                [6.0, 19.5], [8.0, 27], [10.0, 33.3]]
    """Сначала производится расчет коэффициента К"""
    if not 2100 <= Re <= 10000:
        print('Режим не переходный!')
    else:
        Re = Re * 0.001
        for i in k_miheev:
            if i[0] == Re:
                k = i[1]
            else:  # Если такого отношения нет, то делается интерполяция по вышеуказанной функции interpolation
                for j in range(len(k_miheev) - 1):
                    if k_miheev[j + 1][0] > Re > k_miheev[j][0]:
                        k = interpolation(k_miheev[j + 1][1], k_miheev[j][1], k_miheev[j + 1][0], k_miheev[j][0], Re)
        return k * et * Pr ** 0.43


def Nu_turb_count(Re, Pr, et, el):
    """Функция рассчитывает число Нуссельта для турбулентного режима течения (авторы Михеев М.А, Назмеев Ю.Г.)"""
    return 0.021 * (Re ** 0.8) * Pr ** 0.43 * et * el


def koef_teplootdachi(Nu, lyambda, d):
    """Функция рассчитывает коэффициент теплоотдачи"""
    return Nu * lyambda / d


def koef_teploperedachi(alpha1, alpha2, lyambda_steel, delta_l):
    """Функция считает коэффициент теплопередачи через стенку. Для упрощения взята формула для плоской однослойной стенки.
    Впоследствии функция будет усложняться"""
    return 1 / ((1 / alpha1) + (1 / alpha2) + (delta_l / lyambda_steel))
