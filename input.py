from exceptions import InputError


class InputValues:
    def __init__(self):
        self.matter_heat = self.input_matter(state='горячих')
        self.matter_cool = self.input_matter(state='холодных')
        self.space_heat = self.input_space()

        if self.space_heat == 'in':
            self.space_cool = 'out'
        else:
            self.space_cool = 'in'

    @staticmethod
    def input_matter(state):
        available_matters = {'water'}
        print(f'Доступные виды {state} теплоносителей: ', end='')
        print(*available_matters, sep=', ', end='.\n')

        matter = input('Введите тип теплоносителя из предложенного '
                       'списка: ').lower()
        if matter not in available_matters:
            raise InputError('Введено некорректное название теплоносителя, '
                             'либо его нет в списке доступных теплоносителей.')
        print('-' * 69)
        return matter

    @staticmethod
    def input_space():
        space = input('Протекание горячего теплоносителя: трубное или '
                      'межтрубное? ').lower()
        if space not in ('трубное', 'межтрубное'):
            raise InputError('Введено некорректное пространство протекания '
                             'теплоносителя.')
        print('-' * 69)

        if space == 'трубное':
            return 'in'
        return 'out'
