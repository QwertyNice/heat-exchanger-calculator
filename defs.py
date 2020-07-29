from math import pi, log


def interpolation(y_max, y_min, x_max, x_min, x):
    """Функция проводит интерполяцию данных"""
    return (y_max - y_min) / (x_max - x_min) * (x - x_min) + y_min


def w_count(G, d, ro):
    """Функция считает скорость по уравнению неразрывности"""
    return G / (ro * pi * d ** 2 / 4)


def Re_count(w, d, ny):
    """Функция считает число Рейнольдса"""
    return w * d / ny


def pr_count(cp, ro, ny, lambda_):
    """Функция считает число Прандтля"""
    return cp * ro * ny / lambda_


def epsilon_t_count(pr_domain, pr_wall):
    """Функция считает попровку на температуру"""
    return (pr_domain / pr_wall) ** 0.25


def el_lam_count(l, d):
    """Функция считает поправку на участок стабилизации при ламинарном режиме"""
    el_m = [[1, 1.9], [4, 1.7], [5, 1.44], [10, 1.28], [15, 1.18], [20, 1.13], [30, 1.05], [40, 1.02], [50, 1]]
    if l / d >= 50:
        return 1
    elif l / d < 1:
        raise AssertionError('Диаметр превышает значение длины трубы!')
    else:
        for i in el_m:
            if i[0] == l / d:
                return i[1]
            else:  # Если такого отношения нет, то делается интерполяция по вышеуказанной функции interpolation
                for j in range(len(el_m)):
                    if el_m[j + 1][0] > l / d > el_m[j][0]:
                        return interpolation(el_m[j + 1][1], el_m[j][1], el_m[j + 1][0], el_m[j][0], l / d)


def el_turbulent_count(Re, l, d):
    """Функция считает поправку на участок стабилизации при турбулентном режиме"""
    el_m = [[0, 1, 2, 5, 10, 15, 20, 30, 40, 50],
            [10000, 1.65, 1.50, 1.34, 1.23, 1.17, 1.13, 1.07, 1.03, 1],
            [20000, 1.51, 1.4, 1.27, 1.18, 1.13, 1.1, 1.05, 1.02, 1],
            [50000, 1.34, 1.27, 1.18, 1.13, 1.1, 1.08, 1.04, 1.02, 1],
            [100000, 1.28, 1.22, 1.15, 1.1, 1.08, 1.06, 1.03, 1.02, 1],
            [1000000, 1.14, 1.11, 1.08, 1.05, 1.04, 1.03, 1.02, 1.01, 1]]
    for i in range(2, len(el_m)):
        if l / d <= 50 and Re <= 1_000_000:
            if el_m[i - 1][0] <= Re <= el_m[i][0]:
                for j in range(len(el_m[0])):
                    if el_m[0][j] > l / d >= el_m[0][j - 1]:
                        inter_min = interpolation(el_m[i - 1][j], el_m[i - 1][j - 1], el_m[0][j], el_m[0][j - 1], l / d)
                        inter_max = interpolation(el_m[i][j], el_m[i][j - 1], el_m[0][j], el_m[0][j - 1], l / d)
                        return interpolation(inter_max, inter_min, el_m[i][0], el_m[i - 1][0], Re)
        return 1


def nu_lam_count(Re, Pr, et, el):
    """Функция считает число Нуссельта при ламинарном движении (автор Михеев М. А.)"""
    return 0.15 * (Re ** 0.33) * (Pr ** 0.43) * et * el


def nu_per_count(Re, Pr, et):
    Re = Re / 1000
    """Функция производит расчет числа Нуссельта для переходного режима (автор Михеев М.А.)"""
    k_correction = [[2.3, 3.3], [2.4, 3.8], [2.5, 4.4], [3.0, 6.0], [4.0, 10.3],
                    [5.0, 15.5], [6.0, 19.5], [8.0, 27], [10.0, 33.3]]
    for j in range(len(k_correction)):
        if k_correction[j - 1][0] <= Re < k_correction[j][0]:
            return (interpolation(k_correction[j][1], k_correction[j - 1][1],
                                  k_correction[j][0], k_correction[j - 1][0], Re)) * et * Pr ** 0.43


def nu_turbulent_count(Re, Pr, et, el):
    """Функция рассчитывает число Нуссельта для турбулентного режима течения (авторы Михеев М.А, Назмеев Ю.Г.)"""
    return 0.021 * (Re ** 0.8) * Pr ** 0.43 * et * el


def heat_transfer_coefficient(Nu, lyambda, d):
    """Функция рассчитывает коэффициент теплоотдачи"""
    return Nu * lyambda / d


def koef_teploperedachi(alpha1, alpha2, lyambda_steel, delta_l):
    """Функция считает коэффициент теплопередачи через стенку. Для упрощения взята формула для плоской однослойной стенки.
    Впоследствии функция будет усложняться"""
    return 1 / ((1 / alpha1) + (1 / alpha2) + (delta_l / lyambda_steel))


def delta_t_avg(t1_in, t1_out, t2_in, t2_out):
    """Функция считает следнелогарифмическую температурный напор при противотоке(дефолт)"""
    if (t1_in - t2_out) > (t1_out - t2_in):
        return ((t1_in - t2_out) - (t1_out - t2_in)) / log((t1_in - t2_out) / (t1_out - t2_in))
    elif (t1_out - t2_in) > (t1_in - t2_out):
        return ((t1_out - t2_in) - (t1_in - t2_out)) / log((t1_out - t2_in) / (t1_in - t2_out))


def open_exel(t):
    """Вывод теплофизических свойств из экселя"""
    rb = xlrd.open_workbook('C:\\Users\\made\\Desktop\\Теплофизические свойства воды.xls', formatting_info=True)
    sheet = rb.sheet_by_index(0)
    count = 1
    while count < sheet.nrows:
        if sheet.row_values(count)[0] <= t < sheet.row_values(count + 1)[0]:
            yx1 = sheet.row_values(count)
            yx2 = sheet.row_values(count + 1)
            return yx1, yx2
        else:
            count += 1


def heat_exchange_area(G1, c1, t1_in, t1_out, G2, c2, t2_in, t2_out,  K, delta_t):
    if G2 == 0:
        return G1 * c1 * (t1_in - t1_out) * 0.99 / (K * delta_t)
    else:
        return G2 * c2 * (t2_out - t2_in) * 0.99 / (K * delta_t)