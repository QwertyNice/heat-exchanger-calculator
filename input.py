from exceptions import InputError


class InputValues:
    def __init__(self):
        # self.matter_heat = self.input_matter(state='горячих')
        # self.matter_cool = self.input_matter(state='холодных')
        # self.space_heat = self.input_space()
        #
        # if self.space_heat == 'in':
        #     self.space_cool = 'out'
        # else:
        #     self.space_cool = 'in'
        #
        # self.d_out = self.input_d_out()
        # self.delta_l = self.input_delta_l()
        # self.lambda_steel = self.input_lambda_steel()
        self.t_in_heat = self.input_t(in_out='начальной', state='горячего')
        self.t_out_heat = self.input_t(in_out='конечной', state='горячего')
        self.t_in_cool = self.input_t(in_out='начальной', state='холодного')
        self.t_out_cool = self.input_t(in_out='конечной', state='холодного')
        self.check_value_t()

    @staticmethod
    def input_matter(state):
        available_matters = {'water'}
        print(f'Доступные виды {state} теплоносителей: ', end='')
        print(*available_matters, sep=', ', end='.\n')

        matter = input('Введите тип теплоносителя из предложенного '
                       'списка: ').lower()
        if matter not in available_matters:
            message = 'Введено некорректное название теплоносителя, либо ' \
                      'его нет в списке доступных теплоносителей.'
            raise InputError(message)
        print('-' * 69)
        return matter

    @staticmethod
    def input_space():
        space = input('Протекание горячего теплоносителя: трубное или '
                      'межтрубное? ').lower()
        if space not in ('трубное', 'межтрубное'):
            message = 'Введено некорректное пространство протекания ' \
                   'теплоносителя.'
            raise InputError(message)
        print('-' * 69)

        if space == 'трубное':
            return 'in'
        return 'out'

    @staticmethod
    def input_d_out():
        d_out = input('Введите внешний диаметр трубы, мм: ')
        try:
            d_out = float(d_out)
        except ValueError:
            message = f'Введено некорректное значение диаметра: {d_out}.'
            raise InputError(message)
        if d_out <= 0:
            message = 'Введено отрицательное или нулевое значение диаметра.'
            raise InputError(message)
        return d_out

    def input_delta_l(self):
        delta_l = input('Введите толщину трубки, мм: ')
        try:
            delta_l = float(delta_l)
        except ValueError:
            message = f'Введено некорректное значение толщины ' \
                      f'трубки: {delta_l}'
            raise InputError(message)
        if delta_l <= 0:
            message = 'Введено отрицательное или нулевое значение толщины ' \
                      'стенки трубы.'
            raise InputError(message)
        if self.d_out <= 2 * delta_l:
            message = f'Внутренний диаметр трубы меньше или равен нулю: ' \
                      f'{self.d_out - 2*delta_l} мм.'
            raise InputError(message)
        return delta_l

    @staticmethod
    def input_lambda_steel():
        lambda_steel = input('Введите коэффициент теплопроводности металла '
                             'стенки трубы, Вт/(м∙град): ')
        try:
            lambda_steel = float(lambda_steel)
        except ValueError:
            message = f'Введено некорректное значение коэффициента ' \
                      f'теплопроводности металла стенки трубы: ' \
                      f'{lambda_steel}.'
            raise InputError(message)
        if lambda_steel <= 0:
            message = 'Введено отрицательное или нулевое значение ' \
                      'коэффициента теплопроводности металла стенки трубы.'
            raise InputError(message)
        return lambda_steel

    @staticmethod
    def input_t(in_out, state):
        t = input(f'Введите значение {in_out} температуры {state} '
                  f'теплоносителя, °C: ')
        try:
            t = float(t)
        except ValueError:
            message = f'Введено некорректное значение {in_out} температуры ' \
                      f'{state} теплоносителя: {t}'
            raise InputError(message)
        if t < 0:
            message = f'Введено отрицательное значение {in_out} ' \
                      f'температуры {state} теплоносителя.'
            raise InputError(message)
        return t

    def check_value_t(self):
        if self.t_in_heat <= self.t_out_heat:
            message = 'Начальная температура горячего теплоносителя меньше ' \
                      'или равна конечной.'
            raise InputError(message)
        if self.t_in_cool >= self.t_out_heat:
            message = 'Начальная температура холодного теплоносителя больше ' \
                      'или равна конечной.'
            raise InputError(message)
        if not 0 <= (self.t_in_heat + self.t_out_heat) / 2 < 370:
            message = 'Средняя температура потока горячего теплоносителя ' \
                      'выходит за границы 0..370°C'
            raise InputError(message)
        if not 0 <= (self.t_in_cool + self.t_out_cool) / 2 < 370:
            message = 'Средняя температура потока холодного теплоносителя ' \
                      'выходит за границы 0..370°C'
            raise InputError(message)


InputValues()



