import csv
from raw_ver_1.defs import interpolation

def solve_phys_props(t, matter):
        local_dict_phys = dict()
        with open('{}.csv'.format(matter)) as f:
            line_generator = csv.reader(f, delimiter=';')
            next(line_generator)
            symbol_phys = next(line_generator)
            line_generator = list(line_generator)  # Переделать генератор
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

# print(solve_phys_props(150, 'water'))


def test_solve_phys_props(t, matter):
    with open('{}.csv'.format(matter)) as f:
        line_generator = csv.reader(f, delimiter=';')
        next(line_generator)
        symbol_phys = next(line_generator)
        print(symbol_phys)
        tmp = symbol_phys.index('ro')
        low_lvl = next(line_generator)
        high_lvl = next(line_generator)
        while not float(low_lvl[0]) <= t < float(high_lvl[0]):
            low_lvl = high_lvl
            high_lvl = next(line_generator)
        print(low_lvl[0], low_lvl[tmp], high_lvl[0], high_lvl[tmp])

        # line_generator = list(line_generator)  # Переделать генератор
        # # Сделали через лист (помойкак)
        # len_line_generator = len(line_generator)
        # for index in range(len_line_generator):
        #     if float(line_generator[index - 1][0]) <= t < \
        #             float(line_generator[index][0]):
        #         line_generator_min = list(map(float,
        #                                       line_generator[index - 1]))
        #         line_generator_max = list(map(float,
        #                                       line_generator[index]))
        #         for i in range(len(symbol_phys)):
        #             local_dict_phys[symbol_phys[i]] = \
        #                 interpolation(line_generator_max[i],
        #                               line_generator_min[i],
        #                               line_generator_max[0],
        #                               line_generator_min[0], t)
        #         return local_dict_phys

# test_solve_phys_props(45, 'water')
