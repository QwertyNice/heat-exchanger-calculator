from math import log, pi


def interpolation(y_max, y_min, x_max, x_min, x):
    """Функция проводит интерполяцию данных"""
    return (y_max - y_min) / (x_max - x_min) * (x - x_min) + y_min


def utochnenie(pudge, D_in, D_out):
    """Привязываем диаметры к теплоносителям"""
    global d_heat, d_cold, w_heat, w_cold
    if pudge == 1:
        d_heat = D_in
        d_cold = D_out
        w_cold = w2
        w_heat = w_count(G1, d_heat, ro1)
    else:
        d_heat = D_in
        d_cold = D_out
        w_heat = w1
        w_cold = w_count(G2, d_cold, ro2)


def w_count(G, d, ro):
    """Функция считает скорость по уравнению неразрывности"""
    return G / (ro * pi * d ** 2 / 4)


def Re_count(w, d, ny):
    """Функция считает число Рейнольдса"""
    return w * d / ny


def Pr_count(c, ro, ny, lyambda):
    """Функция считает число Прандтля"""
    return c * ro * ny / lyambda


def et_count(Pr, Pr_wall):
    """Функция считает попровку на температуру"""
    return (Pr / Pr_wall) ** 0.25


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
    for i in range(len(el_m)):
        if Re == el_m[i][0]:
            for j in range(0, len(el_m[0])):
                if l / d == el_m[0][j]:
                    return el_m[i][j]
                elif el_m[0][j] > l / d > el_m[0][j - 1]:
                    return interpolation(el_m[i][j], el_m[i][j - 1], el_m[0][j], el_m[0][j - 1], l / d)
                else:
                    return 1
        elif el_m[i][0] > Re > el_m[i - 1][0]:
            for j in range(0, len(el_m[0])):
                if l / d == el_m[0][j]:
                    return interpolation(el_m[i][j], el_m[i - 1][j], el_m[i][0], el_m[i - 1][0], Re)
                elif el_m[0][j] > l / d > el_m[0][j - 1]:
                    inter_min = interpolation(el_m[i - 1][j], el_m[i - 1][j - 1], el_m[0][j], el_m[0][j - 1], l / d)
                    inter_max = interpolation(el_m[i][j], el_m[i][j - 1], el_m[0][j], el_m[0][j - 1], l / d)
                    return interpolation(inter_max, inter_min, el_m[i][0], el_m[i - 1][0], Re)
                else:
                    return 1
        else:
            return 1


def Nu_lam_count(Re, Pr, et, el):
    """Функция считает число Нуссельта при ламинарном движении (автор Назмеев Ю. Г.)"""
    return 0.15 * (Re ** 0.33) * (Pr ** 0.43) * et * el


def Nu_per_count(Re, Pr, et):
    """Функция производит расчет числа Нуссельта для переходного режима (автор Михеев М.А.)"""
    k_miheev = [[2.3, 3.3], [2.4, 3.8], [2.5, 4.4], [3.0, 6.0], [4.0, 10.3], [5.0, 15.5], [6.0, 19.5], [8.0, 27],
                [10.0, 33.3]]
    """Сначала производится расчет коэффициента К"""
    Re = Re * 0.001
    for i in k_miheev:
        if i[0] == Re:
            k = i[1]
        else:
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


def Foo(G1, c1, t1_in, t1_out, G2, c2, t2_in, t2_out,  K, delta_t):
    if G2 == 0:
        return G1 * c1 * (t1_in - t1_out) * 0.99 / (K * delta_t)
    else:
        return G2 * c2 * (t2_out - t2_in) * 0.99 / (K * delta_t)


'''Обозначения входных данных

t1_in - на входе горяч теплоносителя
t1_out - на выходе горяч теплоносителя
t2_in - на входе холодного теплоносителя
t2_out - на выходе холодного теплоносителя
G1 - расход горячего теплоносителя
G2 - расход холодного теплоносителя
D_out - внешний диаметр трубы
delta_l - толщина стенки трубы
lyambda_steel - коэффициент теплопроводности металла стенки трубы
l - длинна теплообменного аппарата


Условия использования программы:
1) Оба теплоносителя - вода
2) Омывание просходит одиночной трубы
3) Омывание происходит под углом 0 град
4) Внешняя скорость всегда определяется как оптимальная (1.5 м/c)
5) Температура стенки пнринимается одинаковой с двух сторон трубы и является средней температурой между
средними температурами потоков
6) Расчет происходить из условия только противотока
7) КПД принимается равным 1, т.к. рассматривается не волноценный теплообменный аппарат
8) Расчет - конструктивный
9) Исправить инфу о длинне трубы (10000)
'''

print('Введите входные величины для расчета:')
D_out = float(input('Внешний диаметр трубы, мм: '))
delta_l = float(input('Толщина стенки трубы, мм: '))
t1_in = float(input('Температура на входе со стороны горячего теплоносителя, °C: '))
t1_out = float(input('Температура на выходе со стороны горячего теплоносителя, °C: '))
t2_in = float(input('Температура на входе со стороны холодного теплоносителя, °C: '))
t2_out = float(input('Температура на выходе со стороны холодного теплоносителя, °C: '))
lyambda_steel = float(input('Коэффициент теплопроводности металла стенки трубы, Вт/(м∙град): '))
print('Предположительная длина трубы (данная величина влияет лишь на расчет участка стабилизации)')
print('В случае, если данную поправку не требуется учитывать, введите: 10000')
l = float(input('Предположительная длина трубы, м: '))

"""Опредление какой из теплоносителетей протекает в трубном пространстве"""
place = input('Укажите какой из теплоносителей протекает в трубном пространстве (горячий или холодный): ')
while place != 'горячий' or place != 'холодный':
    if place == 'горячий':
        pudge = 1
        G1 = float(input('Расход горячего теплоносителя, кг/с: '))
        w2 = float(input('Скорость холодного теплоносителя, м/c: '))
        G2 = 0
        break
    elif place == 'холодный':
        pudge = 2
        G2 = float(input('Расход холодного теплоносителя, кг/с: '))
        w1 = float(input('Скорость горячего теплоносителя, м/c: '))
        G1 = 0
        break
    else:
        place = input('Допущена ошибка в слове "горячий" или "холодный". Введите данные заново: ')

"""Определение теплофизических свойств горячего телоносителя"""
print('--------------------------------------------------------------------------------')
t1_avr = (t1_in + t1_out) / 2
yx1, yx2 = open_exel(t1_avr)
ro1 = interpolation(yx2[1], yx1[1], yx2[0], yx1[0], t1_avr)
print('Плотность горячего теплоносителя, кг/(м∙м∙м):', ro1)
c1 = interpolation(yx2[2], yx1[2], yx2[0], yx1[0], t1_avr)
print('Теплоемкость горячего теплоносителя, Дж/(кг∙град):', c1)
lyambda1 = interpolation(yx2[3], yx1[3], yx2[0], yx1[0], t1_avr)
print('Коэффициент теплопроводности горячего теплоносителя, Дж/(кг∙град):', lyambda1)
ny1 = interpolation(yx2[4], yx1[4], yx2[0], yx1[0], t1_avr)
print('Кинематическая вязкость горячего теплоносителя, (м∙м)/с:', ny1)
betta1 = interpolation(yx2[5], yx1[5], yx2[0], yx1[0], t1_avr)
print('Коэффициент объемного расширения, 1/K:', betta1)
print('--------------------------------------------------------------------------------')

"""Определение теплофизических свойств холодного телоносителя"""
t2_avr = (t2_in + t2_out) / 2
yx1, yx2 = open_exel(t2_avr)
ro2 = interpolation(yx2[1], yx1[1], yx2[0], yx1[0], t2_avr)
print('Плотность холодного теплоносителя, кг/(м∙м∙м):', ro2)
c2 = interpolation(yx2[2], yx1[2], yx2[0], yx1[0], t2_avr)
print('Теплоемкость холодного теплоносителя, Дж/(кг∙град):', c2)
lyambda2 = interpolation(yx2[3], yx1[3], yx2[0], yx1[0], t2_avr)
print('Коэффициент теплопроводности холодного теплоносителя, Дж/(кг∙град):', lyambda2)
ny2 = interpolation(yx2[4], yx1[4], yx2[0], yx1[0], t2_avr)
print('Кинематическая вязкость холодного теплоносителя, (м∙м)/с:', ny2)
betta2 = interpolation(yx2[5], yx1[5], yx2[0], yx1[0], t2_avr)
print('Коэффициент объемного расширения холодного теплоносителя, 1/K:', betta2)
print('--------------------------------------------------------------------------------')

"""Определение теплофизических свойств телоносителя при температуре стенки"""
t_w_avr = (t2_avr + t1_avr) / 2
yx1, yx2 = open_exel(t_w_avr)
ro_w = interpolation(yx2[1], yx1[1], yx2[0], yx1[0], t_w_avr)
print('Плотность теплоносителя при температуре стенки, кг/(м∙м∙м):', ro_w)
c_w = interpolation(yx2[2], yx1[2], yx2[0], yx1[0], t_w_avr)
print('Теплоемкость теплоносителя при температуре стенки, Дж/(кг∙град):', c_w)
lyambda_w = interpolation(yx2[3], yx1[3], yx2[0], yx1[0], t_w_avr)
print('Коэффициент теплопроводности теплоносителя при температуре стенки, Дж/(кг∙град):', lyambda_w)
ny_w = interpolation(yx2[4], yx1[4], yx2[0], yx1[0], t_w_avr)
print('Кинематическая вязкость теплоносителя при температуре стенки, (м∙м)/с:', ny_w)
betta_w = interpolation(yx2[5], yx1[5], yx2[0], yx1[0], t_w_avr)
print('Коэффициент объемного расширения теплоносителя при температуре стенки, 1/K:', betta_w)
print('--------------------------------------------------------------------------------')

D_in = D_out - 2 * delta_l
print('Внутренний диаметр составил:', D_in)

utochnenie(pudge, D_in, D_out)  # Делаем уточнение по диаметрам
Re1 = Re_count(w_heat, d_heat, ny1)
print('Число Рейнольдса горячего теплоносителя составило:', Re1)
Re2 = Re_count(w_cold, d_cold, ny2)
print('Число Рейнольдса холодного теплоносителя составило:', Re2)
Pr1 = Pr_count(c1, ro1, ny1, lyambda1)
print('Число Прадтля горячего теплоносителя составило:', Pr1)
Pr2 = Pr_count(c2, ro2, ny2, lyambda2)
print('Число Прадтля холодного теплоносителя составило:', Pr2)
pr_wall = Pr_count(c_w, ro_w, ny_w, lyambda_w)
et1 = et_count(Pr1, pr_wall)
et2 = et_count(Pr2, pr_wall)

if Re1 < 2300:
    el1 = el_lam_count(l, d_heat)
    Nu1 = Nu_lam_count(Re1, Pr1, et1, el1)
    print('Число Нуссельта горячего теплоносителя составило:', Nu1)
elif 2300 <= Re1 <= 10000:
    Nu1 = Nu_per_count(Re1, Pr1, et1)
    print('Число Нуссельта горячего теплоносителя составило:', Nu1)
else:
    el1 = el_turb_count(Re1, l, d_heat)
    Nu1 = Nu_turb_count(Re1, Pr1, et1, el1)
    print('Число Нуссельта горячего теплоносителя составило:', Nu1)

if Re2 < 2300:
    el2 = el_lam_count(l, d_cold)
    Nu2 = Nu_lam_count(Re2, Pr2, et2, el2)
    print('Число Нуссельта холодного теплоносителя составило:', Nu2)
elif 2300 <= Re2 <= 10000:
    Nu2 = Nu_per_count(Re2, Pr2, et2)
    print('Число Нуссельта холодного теплоносителя составило:', Nu2)
else:
    el2 = el_turb_count(Re2, l, d_cold)
    Nu2 = Nu_turb_count(Re2, Pr2, et2, el2)
    print('Число Нуссельта холодного теплоносителя составило:', Nu2)

alpha1 = koef_teplootdachi(Nu1, lyambda1, d_heat)
print('Коэффициент теплоотдачи от горячего теплоносителя к стенке составил:', alpha1, 'Вт/(м2∙град)')
alpha2 = koef_teplootdachi(Nu2, lyambda2, d_cold)
print('Коэффициент теплоотдачи от стенки к холодному теплоносителю составил:', alpha2, 'Вт/(м2∙град)')
K = koef_teploperedachi(alpha1, alpha2, lyambda_steel, delta_l)
print('Коэффициент теплопередачи составил:', K, 'Вт/(м2∙град)')
delta_t = delta_t_avg(t1_in, t1_out, t2_in, t2_out)
print('Среднелогарифмический температурный напор составил:', delta_t, 'град')
F = Foo(G1, c1, t1_in, t1_out, G2, c2, t2_in, t2_out,  K, delta_t)
print('Площадь теплообмена составила: ', F, 'м2')
