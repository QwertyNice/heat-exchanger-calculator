import csv
import defs
"""Вводные параметры"""
# print('Введите входные величины для расчета:')
# D_out = float(input('Внешний диаметр трубы, мм: '))
# delta_l = float(input('Толщина стенки трубы, мм: '))
# t1_in = float(input('Температура на входе со стороны горячего теплоносителя, °C: '))
# t1_out = float(input('Температура на выходе со стороны горячего теплоносителя, °C: '))
# t2_in = float(input('Температура на входе со стороны холодного теплоносителя, °C: '))
# t2_out = float(input('Температура на выходе со стороны холодного теплоносителя, °C: '))
# lambda_steel = float(input('Коэффициент теплопроводности металла стенки трубы, Вт/(м∙град): '))
# print('Предположительная длина трубы (данная величина влияет лишь на расчет участка стабилизации)')
# print('В случае, если данную поправку не требуется учитывать, введите: 10000')
# l = float(input('Предположительная длина трубы, м: '))


def interpolation(y_max, y_min, x_max, x_min, x):
    """ Функция проводит интерполяцию данных. """
    return (y_max - y_min) / (x_max - x_min) * (x - x_min) + y_min


class TOA:
    """ Осной класс в котором будут инициализироваться инпуты и определять какой параметр надо высчитывать. """

    def __init__(self, D_out, delta_l=None, t1_in=None, t1_out=None,           # Тут я убрал None У D_out
                 t2_in=None, t2_out=None, lambda_steel=None, length=None):
        self.D_out = D_out
        self.delta_l = delta_l
        self.t1_in = t1_in
        self.t1_out = t1_out
        self.t2_in = t2_in
        self.t2_out = t2_out
        self.lambda_steel = lambda_steel
        self.length = length

    # def show_undef_attr(self):
    #     """ Функция выводит ПЕРВЫЙ не присвоенный элемент в окне ввода. """
    #     for key, value in self.__dict__.items():
    #         if not value:
    #             return key


class Domain:
    """ Класс для подсчета характеристик теплоносителя (Nu, Re и тд). """
    def __init__(self, matter, G, w, t_in, t_out, space, D_out, delta_l, length):       # Вводятся внешний диаметр и толщина
        self.D_out = D_out
        self.delta_l = delta_l
        self.space = space
        self.matter = matter
        self.G = G
        self.w = w
        # self.t_in = t_in
        # self.t_out = t_out
        self.t_avr = (t_in + t_out) / 2
        self.length = length
        self.D_in = D_out - 2 * delta_l
        self._dict_phys = self.solve_phys_props()
        self.re = self.solve_re()
        self.pr_domain = self.solve_pr()
        self.nu = self.solve_nu()

    def solve_phys_props(self):                                                 # Посомтреть вызов медода заранее
        """ Функция считывает файл с теплофизическими свойствами и возвращает словарь с
        проинтерполированными величинами при средней температуре потока. """
        local_dict_phys = dict()
        assert 0 <= self.t_avr < 370                                            # Добавили ассер, потом чекнуть
        with open('{}.csv'.format(self.matter)) as f:
            line_generator = csv.reader(f, delimiter=';')
            next(line_generator)
            symbol_phys = next(line_generator)
            line_generator = list(line_generator)                               # Сделали через лист (помойкак)
            len_line_generator = len(line_generator)
            for index in range(len_line_generator):
                if float(line_generator[index - 1][0]) <= self.t_avr < float(line_generator[index][0]):
                    line_generator_min = list(map(float, line_generator[index - 1]))
                    line_generator_max = list(map(float, line_generator[index]))
                    for i in range(len(symbol_phys)):
                        local_dict_phys[symbol_phys[i]] = interpolation(line_generator_max[i],
                                                                        line_generator_min[i],
                                                                        line_generator_max[0],
                                                                        line_generator_min[0], self.t_avr)
                    return local_dict_phys

    def solve_re(self):
        """ Находит число Re для потока жидкости в зависимости от его положения. """
        if self.space == 'in':
            return self.w * self.D_in / self._dict_phys['ny']
        return self.w * self.D_out / self._dict_phys['ny']

    def solve_pr(self):
        """ Находит число Nu для потока жидкости в зависимости от его положения. """
        return self._dict_phys['cp'] * self._dict_phys['ro'] * self._dict_phys['ny'] / self._dict_phys['lambda_']

    def solve_epsilon_l_lam_count(self):
        """ Функция считает поправку на участок стабилизации при ламинарном режиме. """
        if self.space == 'in':
            return defs.el_lam_count(self.length, self.D_in)
        return 1

    def solve_epsilon_l_turbulent_count(self):
        """ Функция считает поправку на участок стабилизации при турбулентном режиме. """
        if self.space == 'in':
            return defs.el_turbulent_count(self.re, self.length, self.D_in)
        return 1

    def solve_epsilon_t_count(self):     # Додумать тему с расчетом температуры стенки икак следствие попарвочного коэфф
        pass

    def solve_nu(self):
        pass


# solve = Domain('water', 5, 2, 100, 50, 'in', 0.05, 0.005, 5)
# print(solve.re)
