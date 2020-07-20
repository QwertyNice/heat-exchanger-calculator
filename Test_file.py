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