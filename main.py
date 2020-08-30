import csv
import math
import defs
from input import InputValues


class LiquidDomain:
    """
    Класс для подсчета характеристик теплоносителя (Nu, Re и тд).
    """
    global_dict_of_domains = {'heat': __name__, 'cool': __name__}

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        cls.global_dict_of_domains[kwargs['state']] = obj
        return obj

    def __init__(self, matter, t_in, t_out, space, d_out, delta_l,
                 length, state, consumption, w, t_avr_w=None):
        # Все плохо
        # Вводятся внешний диаметр и толщина
        self.state = state  # Его роль для dict_of_domains
        self.d_out = d_out
        self.delta_l = delta_l
        self.space = space
        self.matter = matter
        self.t_in = t_in
        self.t_out = t_out
        self.t_avr = (t_in + t_out) / 2
        self.t_avr_w = t_avr_w or self.t_avr
        self.length = length
        self.d_in = d_out - 2*delta_l
        self.dict_phys = self.solve_phys_props(t=self.t_avr,
                                               matter=self.matter)

        if t_avr_w is None:
            self.dict_phys_wall = self.dict_phys
        else:
            self.dict_phys_wall = self.solve_phys_props(t=self.t_avr_w,
                                                        matter=self.matter)

        self.consumption = consumption or (math.pi * self.d_in**2 *
                                           self.dict_phys['ro']) / 4
        self.w = w or ((4 * consumption) /
                       (math.pi * self.d_in**2 * self.dict_phys['ro']))
        # Расход и скорость для условия потока В ТРУБЕ
        self.re = self.solve_re()
        self.pr_domain = self.solve_pr(self.dict_phys)
        self.pr_wall = self.solve_pr(self.dict_phys_wall)
        self.nu = self.solve_nu()
        self.heat_coefficient = self.solve_heat_coefficient()

    @staticmethod
    def solve_phys_props(t, matter):     # Посмотреть вызов медода заранее
        """
        Функция считывает файл с теплофизическими свойствами и
        возвращает словарь с проинтерполированными величинами при средней
        температуре потока.
        """
        local_dict_phys = dict()
        assert 0 <= t < 370           # Добавили ассер, потом чекнуть
        with open('{}.csv'.format(matter)) as f:
            line_generator = csv.reader(f, delimiter=';')
            next(line_generator)
            symbol_phys = next(line_generator)
            line_generator = list(line_generator)  # Переделать генератор
            # Сделали через лист (помойкак)
            len_line_generator = len(line_generator)
            for index in range(len_line_generator):
                if float(line_generator[index - 1][0]) <= t < \
                        float(line_generator[index][0]):
                    line_generator_min = list(map(float,
                                                  line_generator[index - 1]))
                    line_generator_max = list(map(float,
                                                  line_generator[index]))
                    for i in range(len(symbol_phys)):
                        local_dict_phys[symbol_phys[i]] = \
                            interpolation(line_generator_max[i],
                                          line_generator_min[i],
                                          line_generator_max[0],
                                          line_generator_min[0], t)
                    return local_dict_phys

    def solve_re(self):
        """
        Находит число Re для потока жидкости в зависимости от его положения.
        """
        if self.space == 'in':
            return self.w * self.d_in / self.dict_phys['ny']
        return self.w * self.d_out / self.dict_phys['ny']

    @staticmethod
    def solve_pr(dict_phys):
        """
        Находит число Nu для потока жидкости в зависимости от его положения.
        """
        return defs.pr_count(cp=dict_phys['cp'], ro=dict_phys['ro'],
                             ny=dict_phys['ny'], lambda_=dict_phys['lambda_'])

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

    def solve_epsilon_t_count(self):
        # Додумать тему с расчетом температуры стенки,
        # как следствие попарвочного коэфф
        if self.t_avr_w == self.t_avr:
            return 1
        else:
            return defs.epsilon_t_count(pr_domain=self.pr_domain,
                                        pr_wall=self.pr_wall)

    def solve_nu(self):  # Ассерт при Re < 0 добавить
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
            return defs.nu_turbulent_count(
                self.re, self.pr_domain, self.solve_epsilon_t_count(),
                self.solve_epsilon_l_turbulent_count())

    def solve_heat_coefficient(self):
        """
        Находит коэффициент теплоотдачи для потока жидкости в зависимости от
        его положения.
        """
        if self.space == 'in':
            return defs.heat_transfer_coefficient(self.nu,
                                                  self.dict_phys['lambda_'],
                                                  self.d_in)
        else:
            return defs.heat_transfer_coefficient(self.nu,
                                                  self.dict_phys['lambda_'],
                                                  self.d_out)


class HeatExchangerSolver:
    """
    Основной класс в котором будут инициализироваться инпуты и определять какой
    параметр надо высчитывать.
    """

    def __init__(self, dict_of_domains, lambda_steel):
        # Тут я убрал None У D_out
        self.dict_of_domains = dict_of_domains
        self.alpha_heat = dict_of_domains['heat'].heat_coefficient
        self.alpha_cool = dict_of_domains['cool'].heat_coefficient
        self.lambda_steel = lambda_steel
        self.delta_l = dict_of_domains['cool'].delta_l
        self.t_in_heat = dict_of_domains['heat'].t_in
        self.t_out_heat = dict_of_domains['heat'].t_out
        self.t_in_cool = dict_of_domains['cool'].t_in
        self.t_out_cool = dict_of_domains['cool'].t_out
        self.heat_transfer_coefficient = self.solve_heat_transfer_coefficient()
        self.avg_log_delta_temperature = self.solve_avg_log_delta_temperature()
        self.heat_exchange_area = self.solve_heat_exchange_area()

    def solve_heat_transfer_coefficient(self):
        return 1 / ((1 / self.alpha_heat) + (1 / self.alpha_cool) +
                    (self.delta_l / self.lambda_steel))

    def solve_avg_log_delta_temperature(self):
        return defs.delta_t_avg(t1_in=self.t_in_heat, t1_out=self.t_out_heat,
                                t2_in=self.t_in_cool, t2_out=self.t_out_cool)

    def solve_heat_exchange_area(self):
        return self.dict_of_domains['heat'].consumption * \
               self.dict_of_domains['heat'].dict_phys['cp'] * \
               (self.t_in_heat - self.t_out_heat) / \
               (self.heat_transfer_coefficient *
                self.avg_log_delta_temperature)


class SuccessiveApproximation:
    """"
    Класс, который проводит последовательное приближение температуры стенки к
    фактическому значению с погрешностью не более 5%
    """
    def __init__(self, dict_of_domains, obj_solver_toa):
        self.obj_solver_toa = obj_solver_toa
        self.dict_of_domains = dict_of_domains
        self.avg_log_delta_temperature = \
            obj_solver_toa.avg_log_delta_temperature
        self.heat_transfer_coefficient = \
            obj_solver_toa.heat_transfer_coefficient

    def approximation(self):
        t_avg_heat_wall = self.dict_of_domains['heat'].t_avr - \
            self.heat_transfer_coefficient * \
            self.avg_log_delta_temperature / \
            self.dict_of_domains['heat'].heat_coefficient

        t_avg_cool_wall = self.dict_of_domains['cool'].t_avr + \
            self.heat_transfer_coefficient * \
            self.avg_log_delta_temperature / \
            self.dict_of_domains['cool'].heat_coefficient

        error_heat = (self.dict_of_domains['heat'].t_avr - t_avg_heat_wall) / \
            self.dict_of_domains['heat'].t_avr
        error_cool = (t_avg_cool_wall - self.dict_of_domains['cool'].t_avr) / \
            t_avg_cool_wall

        while (error := max(error_heat, error_cool)) > 0.05:
            obj_heat = self.dict_of_domains['heat']
            obj_cool = self.dict_of_domains['cool']
            t_avg_heat_wall_prev = t_avg_heat_wall
            t_avg_cool_wall_prev = t_avg_cool_wall

            obj_heat.__init__(matter=obj_heat.matter, t_in=obj_heat.t_in,
                              t_out=obj_heat.t_out, space=obj_heat.space,
                              d_out=obj_heat.d_out, delta_l=obj_heat.delta_l,
                              length=obj_heat.length,
                              consumption=obj_heat.consumption, w=obj_heat.w,
                              state=obj_heat.state, t_avr_w=t_avg_heat_wall)

            obj_cool.__init__(matter=obj_cool.matter, t_in=obj_cool.t_in,
                              t_out=obj_cool.t_out, space=obj_cool.space,
                              d_out=obj_cool.d_out, delta_l=obj_cool.delta_l,
                              length=obj_cool.length,
                              consumption=obj_cool.consumption, w=obj_cool.w,
                              state=obj_cool.state, t_avr_w=t_avg_cool_wall)

            self.obj_solver_toa.__init__(
                dict_of_domains=LiquidDomain.global_dict_of_domains,
                lambda_steel=self.obj_solver_toa.lambda_steel)

            self.__init__(dict_of_domains=LiquidDomain.global_dict_of_domains,
                          obj_solver_toa=self.obj_solver_toa)

            t_avg_heat_wall = obj_heat.t_avr - \
                (self.heat_transfer_coefficient *
                 self.avg_log_delta_temperature /
                 obj_heat.heat_coefficient)

            t_avg_cool_wall = obj_cool.t_avr + \
                (self.heat_transfer_coefficient *
                 self.avg_log_delta_temperature /
                 obj_cool.heat_coefficient)

            error_heat = (t_avg_heat_wall_prev -
                          t_avg_heat_wall) / t_avg_heat_wall_prev
            error_cool = (t_avg_cool_wall -
                          t_avg_cool_wall_prev) / t_avg_cool_wall

        return error


def interpolation(y_max, y_min, x_max, x_min, x):
    """
    Функция проводит интерполяцию данных.
    """
    return (y_max - y_min) / (x_max - x_min) * (x - x_min) + y_min


if __name__ == '__main__':
    inputs = InputValues()

    domain_heat = LiquidDomain(matter=inputs.matter_heat,
                               t_in=inputs.t_in_heat,
                               t_out=inputs.t_out_heat,
                               space=inputs.space_heat,
                               d_out=inputs.d_out, delta_l=inputs.delta_l,
                               length=inputs.length, state='heat',
                               consumption=inputs.consumption_heat,
                               w=inputs.w_heat)

    domain_cool = LiquidDomain(matter=inputs.matter_cool,
                               t_in=inputs.t_in_cool,
                               t_out=inputs.t_out_cool,
                               space=inputs.space_cool,
                               d_out=inputs.d_out, delta_l=inputs.delta_l,
                               length=inputs.length, state='cool',
                               consumption=inputs.consumption_cool,
                               w=inputs.w_cool)

    # domain_heat = LiquidDomain(matter='water', t_in=100,
    #                      t_out=50, space='in',
    #                      d_out=0.100, delta_l=0.002,
    #                      length=6, state='heat',
    #                      consumption=None, w=2)
    #
    # domain_cool = LiquidDomain(matter='water', t_in=20,
    #                      t_out=50, space='out',
    #                      d_out=0.100, delta_l=0.002,
    #                      length=6, state='cool',
    #                      consumption=None, w=2)

    heat_exchanger_solver = HeatExchangerSolver(
        dict_of_domains=LiquidDomain.global_dict_of_domains,
        lambda_steel=55)

    SuccessiveApproximation(
        dict_of_domains=LiquidDomain.global_dict_of_domains,
        obj_solver_toa=heat_exchanger_solver).approximation()

    print(f"Площадь теплообмена составила: "
          f"{heat_exchanger_solver.heat_exchange_area:.3f} м^2")
