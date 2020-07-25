import csv
import math
import defs


class Domain:
    """
    Класс для подсчета характеристик теплоносителя (Nu, Re и тд).
    """
    local_dict_of_domains = {'heat': None, 'cool': None}

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        cls.local_dict_of_domains[kwargs['state']] = obj  # TODO добавка в словарь
        return obj

    def __init__(self, matter, state,  t_in, t_out, space, d_out, delta_l,
                 length, consumption=None, w=None):  # TODO
        # Вводятся внешний диаметр и толщина
        self.state = state  # Его роль для dict_of_domains
        self.d_out = d_out
        self.delta_l = delta_l
        self.space = space
        self.matter = matter
        self.t_avr = (t_in + t_out) / 2
        self.length = length
        self.d_in = d_out - 2 * delta_l
        self._dict_phys = self.solve_phys_props()
        self.w = w or ((4 * consumption) /
                       (math.pi * self.d_in ** 2 * self._dict_phys['ro']))
        # Расход для условия потока В ТРУБЕ
        self.re = self.solve_re()
        self.pr_domain = self.solve_pr()
        self.nu = self.solve_nu()
        self.heat_coefficient = self.solve_heat_coefficient()

    def solve_phys_props(self):              # Посомтреть вызов медода заранее
        """
        Функция считывает файл с теплофизическими свойствами и
        возвращает словарь с проинтерполированными величинами при средней
        температуре потока.
        """
        local_dict_phys = dict()
        assert 0 <= self.t_avr < 370           # Добавили ассер, потом чекнуть
        with open('{}.csv'.format(self.matter)) as f:
            line_generator = csv.reader(f, delimiter=';')
            next(line_generator)
            symbol_phys = next(line_generator)
            line_generator = list(line_generator)  # TODO
            # Сделали через лист (помойкак)
            len_line_generator = len(line_generator)
            for index in range(len_line_generator):
                if float(line_generator[index - 1][0]) <= self.t_avr < \
                        float(line_generator[index][0]):
                    line_generator_min = list(map(float, line_generator[index - 1]))
                    line_generator_max = list(map(float, line_generator[index]))
                    for i in range(len(symbol_phys)):
                        local_dict_phys[symbol_phys[i]] = \
                            interpolation(line_generator_max[i],
                                          line_generator_min[i],
                                          line_generator_max[0],
                                          line_generator_min[0], self.t_avr)
                    return local_dict_phys

    def solve_re(self):
        """
        Находит число Re для потока жидкости в зависимости от его положения.
        """
        if self.space == 'in':
            return self.w * self.d_in / self._dict_phys['ny']
        return self.w * self.d_out / self._dict_phys['ny']

    def solve_pr(self):
        """
        Находит число Nu для потока жидкости в зависимости от его положения.
        """
        return self._dict_phys['cp'] * self._dict_phys['ro'] * self._dict_phys['ny'] / self._dict_phys['lambda_']

    def solve_epsilon_l_lam_count(self):
        """
        Функция считает поправку на участок стабилизации при ламинарном режиме.
        """
        if self.space == 'in':
            return defs.el_lam_count(self.length, self.d_in)
        return 1

    def solve_epsilon_l_turbulent_count(self):
        """
        Функция считает поправку на участок стабилизации при турбулентном
        режиме.
        """
        if self.space == 'in':
            return defs.el_turbulent_count(self.re, self.length, self.d_in)
        return 1

    def solve_epsilon_t_count(self):  # TODO
        # Додумать тему с расчетом температуры стенки,
        # как следствие попарвочного коэфф
        pass

    def solve_nu(self):  # TODO Ассерт при Re < 0 добавить
        """
        Находит число Nu для потока жидкости в зависимости от его положения.
        """
        if self.re < 2300:
            return defs.nu_lam_count(self.re, self.pr_domain,
                                     self.solve_epsilon_t_count(),
                                     self.solve_epsilon_l_lam_count())
        elif 2300 <= self.re < 10_000:
            return defs.nu_per_count(self.re, self.pr_domain,
                                     self.solve_epsilon_t_count())
        else:
            return defs.nu_turbulent_count(self.re, self.pr_domain,
                                           self.solve_epsilon_t_count(),
                                           self.solve_epsilon_l_turbulent_count())

    def solve_heat_coefficient(self):
        """
        Находит коэффициент теплоотдачи для потока жидкости в зависимости от
        его положения.
        """
        if self.space == 'in':
            return defs.heat_transfer_coefficient(self.nu,
                                                  self._dict_phys['lambda_'],
                                                  self.d_in)
        else:
            return defs.heat_transfer_coefficient(self.nu,
                                                  self._dict_phys['lambda_'],
                                                  self.d_out)


class SolverTOA:  # TODO переименовать
    """
    Осной класс в котором будут инициализироваться инпуты и определять какой
    параметр надо высчитывать.
    """

    def __init__(self, dict_of_domains, lambda_steel):
        # TODO Тут я убрал None У D_out
        # self.dict_of_domains = dict_of_domains
        self.alpha_heat = dict_of_domains['heat'].alpha1
        self.alpha_cool = dict_of_domains['cool'].alpha2
        self.lambda_steel = lambda_steel
        self.delta_l = dict_of_domains['cool'].delta_l

    def solve_heat_transfer_coefficient(self):
        return 1 / ((1 / self.alpha_heat) + (1 / self.alpha_cool) +
                    (self.delta_l / self.lambda_steel))


class Test:
    dict_of_domains = {'heat': __name__, 'cool': __name__}  # Чтобы не ругался

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        cls.dict_of_domains[kwargs['state']] = obj
        return obj

    def __init__(self, alpha1, state):
        self.alpha1 = alpha1
        self.state = state


def interpolation(y_max, y_min, x_max, x_min, x):
    """
    Функция проводит интерполяцию данных.
    """
    return (y_max - y_min) / (x_max - x_min) * (x - x_min) + y_min






def input_values():
    """
    Вводные параметры
    """
    print('Введите входные величины для расчета:')
    D_out = float(input('Внешний диаметр трубы, мм: '))
    delta_l = float(input('Толщина стенки трубы, мм: '))
    t1_in = float(input('Температура на входе со стороны горячего теплоносителя, °C: '))
    t1_out = float(input('Температура на выходе со стороны горячего теплоносителя, °C: '))
    t2_in = float(input('Температура на входе со стороны холодного теплоносителя, °C: '))
    t2_out = float(input('Температура на выходе со стороны холодного теплоносителя, °C: '))
    lambda_steel = float(input('Коэффициент теплопроводности металла стенки трубы, Вт/(м∙град): '))
    print('Предположительная длина трубы (данная величина влияет лишь на расчет участка стабилизации)')
    print('В случае, если данную поправку не требуется учитывать, введите: 10000')
    l = float(input('Предположительная длина трубы, м: '))


def main():
    pass


if __name__ == '__main__':
    SolverTOA(Test.dict_of_domains['heat'].alpha1, )
    print(Test.dict_of_domains)
    domain1 = Test(1, state='cool')
    domain2 = Test(2, state='heat')
    print(__name__.alpha1)
    print(Test.dict_of_domains['heat'].alpha1)