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
