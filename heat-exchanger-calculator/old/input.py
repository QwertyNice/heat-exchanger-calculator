from exceptions import InputError, CustomError


class InputValues:
    def __init__(self):
        self.matter_heat = self.input_matter(state='горячих')
        self.matter_cool = self.input_matter(state='холодных')
        self.space_heat = self.input_space()

        if self.space_heat == 'in':
            self.space_cool = 'out'
        else:
            self.space_cool = 'in'
        self.d_out = self.input_d_out()
        self.delta_l = self.input_delta_l()
        self.lambda_steel = self.input_lambda_steel()
        self.t_in_heat = self.input_t(in_out='начальной', state='горячего')
        self.t_out_heat = self.input_t(in_out='конечной', state='горячего')
        self.t_in_cool = self.input_t(in_out='начальной', state='холодного')
        self.t_out_cool = self.input_t(in_out='конечной', state='холодного')
        self.check_value_t()
        self.length = self.input_length()
        self.w_heat, self.consumption_heat = self.input_w_or_consumption(
            state='горячего', space=self.space_heat)
        self.w_cool, self.consumption_cool = self.input_w_or_consumption(
            state='холодного', space=self.space_cool)

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
        print('-' * 69)
        return d_out / 1000

    def input_delta_l(self):
        delta_l = input('Введите толщину трубки, мм: ')
        try:
            delta_l = float(delta_l)
        except ValueError:
            message = f'Введено некорректное значение толщины ' \
                      f'трубки: {delta_l}'
            raise InputError(message)
        delta_l /= 1000
        if delta_l <= 0:
            message = 'Введено отрицательное или нулевое значение толщины ' \
                      'стенки трубы.'
            raise InputError(message)
        if self.d_out <= 2 * delta_l:
            message = f'Внутренний диаметр трубы меньше или равен нулю: ' \
                      f'{self.d_out - 2*delta_l} мм.'
            raise InputError(message)
        print('-' * 69)
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
        print('-' * 69)
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
        print('-' * 69)
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

    def input_length(self):
        print('Введите предположительную длину трубы, м. Если значение '
              'неизвестно, введите рекомендованное: 6 м.')
        length = input('Предположительная длина трубы, м: ')
        try:
            length = float(length)
        except ValueError:
            message = f'Введено некорректное значение длины трубы: {length}.'
            raise InputError(message)
        if length <= 0:
            message = 'Введено отрицательное или нулевое значение длины трубы.'
            raise InputError(message)
        if self.d_out >= length:
            message = 'Введенная длина меньше или равна внешнему диаметру ' \
                      'трубы.'
            raise InputError(message)
        print('-' * 69)
        return length

    @staticmethod
    def input_w_or_consumption(state, space):
        input_temp = input(f'Какая характеристика {state} теплоносителя '
                           f'известна: скорость или расход? ').lower()
        if input_temp not in ('скорость', 'расход'):
            message = f'Введена некорректная характеристика {state} ' \
                      f'теплоносителя.'
            raise InputError(message)
        if input_temp == 'скорость':
            w = input(f'Введите скорость {state} теплоносителя, м/c: ')
            try:
                w = float(w)
            except ValueError:
                message = f'Введено некорректное значение скорости {state} ' \
                          f'теплоносителя.'
                raise InputError(message)
            if w <= 0:
                message = f'Введено отрицательное или нулевое значение ' \
                          f'скорости {state} теплоносителя.'
                raise InputError(message)
            consumption = None
            print('-' * 69)
            return w, consumption
        elif input_temp == 'расход':
            if space == 'in':
                consumption = input(f'Введите расход {state} теплоносителя, '
                                    f'кг/c: ')
                try:
                    consumption = float(consumption)
                except ValueError:
                    message = f'Введено некорректное значение расхода ' \
                              f'{state} теплоносителя.'
                    raise InputError(message)
                if consumption <= 0:
                    message = f'Введено отрицательное или нулевое значение ' \
                              f'расхода {state} теплоносителя.'
                    raise InputError(message)
                w = None
                print('-' * 69)
                return w, consumption
            elif space == 'out':
                message = 'Не предусмотрен расчет расхода без известного ' \
                          'значения диаметра кожуха теплообменного аппарата'
                raise CustomError(message)
