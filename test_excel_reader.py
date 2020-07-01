import xlrd
<<<<<<< HEAD
=======


>>>>>>> origin/master
def interpolation(y_max, y_min, x_max, x_min, x):
    """Функция проводит интерполяцию данных"""
    return (y_max - y_min) / (x_max - x_min) * (x - x_min) + y_min



rb = xlrd.open_workbook('C:\\Users\\made\\Desktop\\Теплофизические свойства воды.xls', formatting_info=True)
sheet = rb.sheet_by_index(0)
count = 1
while count < sheet.nrows:
    if sheet.row_values(count)[0] <= a < sheet.row_values(count + 1)[0]:
        yx1 = sheet.row_values(count)
        yx2 = sheet.row_values(count + 1)
        break
    else:
        count += 1
print(interpolation(yx2[1], yx1[1], yx2[0], yx1[0], a))
