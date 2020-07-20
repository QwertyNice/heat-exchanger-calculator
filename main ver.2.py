import csv


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
    """Функция проводит интерполяцию данных"""
    return (y_max - y_min) / (x_max - x_min) * (x - x_min) + y_min



class TOA:
    """Осной класс в котором будут инициализироваться инпуты и определять какой параметр надо высчитывать"""

    def __init__(self, D_out=None, delta_l=None, t1_in=None, t1_out=None,
                 t2_in=None, t2_out=None, lyambda_steel=None, l=None):
        self.D_out = D_out
        self.delta_l = delta_l
        self.t1_in = t1_in
        self.t1_out = t1_out
        self.t2_in = t2_in
        self.t2_out = t2_out
        self.lyambda_steel = lyambda_steel
        self.l = l

    def show_undef_attr(self):
        """Функция выводит ПЕРВЫЙ не присвоенный элемент в окне ввода"""
        for key, value in self.__dict__.items():
            if not value:
                return key

    # def solve(self):
    #     if self.D_out is None:
    #         solving = Solve_(self.__dict__)


class Domain:
    """Класс для подсчета характеристик теплоносителя (Nu, Re и тд)"""

    def __init__(self, matter, G, w, t_in, t_out):
        self.matter = matter
        self.G = G
        self.w = w
        self.t_in = t_in
        self.t_out = t_out
        self.t_avr = (t_in + t_out) / 2
        self._dict_phys = dict()

    def phys_props(self):
        assert 0 <= self.t_avr < 370                           # Добавили ассер, потом чекнуть
        with open('{}.csv'.format(self.matter)) as f:
            line_generator = csv.reader(f, delimiter=';')
            next(line_generator)
            symbol_phys = next(line_generator)
            line_generator = list(line_generator)              # Сделали через лист (помойкак)
            len_line_generator = len(line_generator)
            for index in range(len_line_generator):
                if float(line_generator[index - 1][0]) <= self.t_avr < float(line_generator[index][0]):
                    line_generator_min = list(map(float, line_generator[index - 1]))
                    line_generator_max = list(map(float, line_generator[index]))
                    for i in range(len(symbol_phys)):
                        self._dict_phys[symbol_phys[i]] = interpolation(line_generator_max[i],
                                                                   line_generator_min[i],
                                                                   line_generator_max[0],
                                                                   line_generator_min[0], self.t_avr)
                    return line_generator_min, line_generator_max


# class SolveSquare:
#
#     def __init__(self, toa):
#         self.a = toa.__dict__
#
#
# toa = TOA()
#
# solve = SolveSquare(toa)
# print(solve.a)
# # toa.show_undef_attr()









