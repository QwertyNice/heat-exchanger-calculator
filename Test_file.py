# import csv
#
#
# def interpolation(y_max, y_min, x_max, x_min, x):
#     """Функция проводит интерполяцию данных"""
#     return (y_max - y_min) / (x_max - x_min) * (x - x_min) + y_min
#
# _dict_phys = {}
#
# def phys_props():
#     t_avr = 340
#     assert 0 <= t_avr < 370  # Добавили ассер, потом чекнуть
#     with open('C:\\Users\\QwertyNice\\Desktop\\Вода.csv') as f:
#         line_generator = csv.reader(f, delimiter=';')
#         next(line_generator)
#         symbol_phys = next(line_generator)
#         line_generator = list(line_generator)  # Сделали через лист (помойка)
#         len_line_generator = len(line_generator)
#         for index in range(len_line_generator):
#             if float(line_generator[index - 1][0]) <= t_avr < float(line_generator[index][0]):
#                 line_generator_min = list(map(float, line_generator[index - 1]))
#                 line_generator_max = list(map(float, line_generator[index]))
#                 for i in range(len(symbol_phys)):
#                     _dict_phys[symbol_phys[i]] = interpolation(line_generator_max[i],
#                                                                 line_generator_min[i],
#                                                                 line_generator_max[0],
#                                                                 line_generator_min[0], t_avr)
#                 return line_generator_min, line_generator_max
#
#
# print(phys_props())
# print(_dict_phys)

from defs import interpolation


# def el_turbulent_count(Re, l, d):
#     """Функция считает поправку на участок стабилизации при турбулентном режиме"""
#     el_m = [[0, 1, 2, 5, 10, 15, 20, 30, 40, 50],
#             [10000, 1.65, 1.50, 1.34, 1.23, 1.17, 1.13, 1.07, 1.03, 1],
#             [20000, 1.51, 1.4, 1.27, 1.18, 1.13, 1.1, 1.05, 1.02, 1],
#             [50000, 1.34, 1.27, 1.18, 1.13, 1.1, 1.08, 1.04, 1.02, 1],
#             [100000, 1.28, 1.22, 1.15, 1.1, 1.08, 1.06, 1.03, 1.02, 1],
#             [1000000, 1.14, 1.11, 1.08, 1.05, 1.04, 1.03, 1.02, 1.01, 1]]
#     for i in range(2, len(el_m)):
#         if l / d <= 50 and Re <= 1_000_000:
#             if el_m[i - 1][0] <= Re <= el_m[i][0]:
#                 for j in range(len(el_m[0])):
#                     if el_m[0][j] > l / d >= el_m[0][j - 1]:
#                         inter_min = interpolation(el_m[i - 1][j], el_m[i - 1][j - 1], el_m[0][j], el_m[0][j - 1], l / d)
#                         inter_max = interpolation(el_m[i][j], el_m[i][j - 1], el_m[0][j], el_m[0][j - 1], l / d)
#                         return interpolation(inter_max, inter_min, el_m[i][0], el_m[i - 1][0], Re)
#         return 1
