import matplotlib.pyplot as plt
from xlrd import open_workbook
import xlsxwriter
import numpy as np

file_name = '../result_draw/v8.0_timeframe_fee.xlsx'
workbook = xlsxwriter.Workbook(file_name)
worksheet = workbook.add_worksheet()
X = [5, 6, 7, 8, 9, 10, 11]
column = 4

book1 = open_workbook('../results/result_v8.5.xls')
book2 = open_workbook('../results/result_v8.6.xls')
book3 = open_workbook('../results/result_v8.7.xls')
book4 = open_workbook('../results/result_v8.8.xls')
book5 = open_workbook('../results/result_v8.9_2.xls')
book6 = open_workbook('../results/result_v8.10_2.xls')
book7 = open_workbook('../results/result_v8.11.xls')
# book8 = open_workbook('../results/result_v8.12.xls')
# book9 = open_workbook('../results/result_v8.13.xls')

sheet1 = book1.sheet_by_index(0)
sheet2 = book2.sheet_by_index(0)
sheet3 = book3.sheet_by_index(0)
sheet4 = book4.sheet_by_index(0)
sheet5 = book5.sheet_by_index(0)
sheet6 = book6.sheet_by_index(0)
sheet7 = book7.sheet_by_index(0)
# sheet8 = book8.sheet_by_index(0)
# sheet9 = book9.sheet_by_index(0)

Y1miner = []
Y11, Y12, Y13, Y14, Y15, Y16, Y17, Y18, Y19 = [], [], [], [], [], [], [], [], []
for row_index in xrange(7000, 9000):
    Y11.append(float(sheet1.cell_value(row_index, column)))
    Y12.append(float(sheet2.cell_value(row_index, column)))
    Y13.append(float(sheet3.cell_value(row_index, column)))
    Y14.append(float(sheet4.cell_value(row_index, column)))
    Y15.append(float(sheet5.cell_value(row_index, column)))
    Y16.append(float(sheet6.cell_value(row_index, column)))
    Y17.append(float(sheet7.cell_value(row_index, column)))
    # Y18.append(float(sheet8.cell_value(row_index, column)))
    # Y19.append(float(sheet9.cell_value(row_index, column)))


Y1miner.append(np.mean(Y11))
Y1miner.append(np.mean(Y12))
Y1miner.append(np.mean(Y13))
Y1miner.append(np.mean(Y14))
Y1miner.append(np.mean(Y15))
Y1miner.append(np.mean(Y16))
Y1miner.append(np.mean(Y17))
# Y1miner.append(np.mean(Y18))
# Y1miner.append(np.mean(Y19))

worksheet.write(1, 0, str(Y1miner[0]))
worksheet.write(2, 0, str(Y1miner[1]))
worksheet.write(3, 0, str(Y1miner[2]))
worksheet.write(4, 0, str(Y1miner[3]))
worksheet.write(5, 0, str(Y1miner[4]))
worksheet.write(6, 0, str(Y1miner[5]))
worksheet.write(7, 0, str(Y1miner[6]))
# worksheet.write(8, 0, str(Y1miner[7]))
# worksheet.write(9, 0, str(Y1miner[8]))

print(Y1miner)

book21 = open_workbook('../results/result_rand_v8.5.xls')
book22 = open_workbook('../results/result_rand_v8.6.xls')
book23 = open_workbook('../results/result_rand_v8.7.xls')
book24 = open_workbook('../results/result_rand_v8.8.xls')
book25 = open_workbook('../results/result_rand_v8.9.xls')
book26 = open_workbook('../results/result_rand_v8.10.xls')
book27 = open_workbook('../results/result_rand_v8.11.xls')
# book28 = open_workbook('../results/result_rand_v8.12.xls')
# book29 = open_workbook('../results/result_rand_v8.13.xls')

sheet21 = book21.sheet_by_index(0)
sheet22 = book22.sheet_by_index(0)
sheet23 = book23.sheet_by_index(0)
sheet24 = book24.sheet_by_index(0)
sheet25 = book25.sheet_by_index(0)
sheet26 = book26.sheet_by_index(0)
sheet27 = book27.sheet_by_index(0)
# sheet28 = book28.sheet_by_index(0)
# sheet29 = book29.sheet_by_index(0)

Y2miner = []
Y21, Y22, Y23, Y24, Y25, Y26, Y27, Y28, Y29 = [], [], [], [], [], [], [], [], []
for row_index in xrange(100, 400):
    Y21.append(float(sheet21.cell_value(row_index, column)))
    Y22.append(float(sheet22.cell_value(row_index, column)))
    Y23.append(float(sheet23.cell_value(row_index, column)))
    Y24.append(float(sheet24.cell_value(row_index, column)))
    Y25.append(float(sheet25.cell_value(row_index, column)))
    Y26.append(float(sheet26.cell_value(row_index, column)))
    Y27.append(float(sheet27.cell_value(row_index, column)))
    # Y28.append(float(sheet28.cell_value(row_index, column)))
    # Y29.append(float(sheet29.cell_value(row_index, column)))

Y2miner.append(np.mean(Y21))
Y2miner.append(np.mean(Y22))
Y2miner.append(np.mean(Y23))
Y2miner.append(np.mean(Y24))
Y2miner.append(np.mean(Y25))
Y2miner.append(np.mean(Y26))
Y2miner.append(np.mean(Y27))
# Y2miner.append(np.mean(Y28))
# Y2miner.append(np.mean(Y29))

worksheet.write(1, 1, str(Y2miner[0]))
worksheet.write(2, 1, str(Y2miner[1]))
worksheet.write(3, 1, str(Y2miner[2]))
worksheet.write(4, 1, str(Y2miner[3]))
worksheet.write(5, 1, str(Y2miner[4]))
worksheet.write(6, 1, str(Y2miner[5]))
worksheet.write(7, 1, str(Y2miner[6]))
# worksheet.write(8, 1, str(Y2miner[7]))
# worksheet.write(9, 1, str(Y2miner[8]))

print(Y2miner)

book31 = open_workbook('../results/result_htt_v8.5.xls')
book32 = open_workbook('../results/result_htt_v8.6.xls')
book33 = open_workbook('../results/result_htt_v8.7.xls')
book34 = open_workbook('../results/result_htt_v8.8.xls')
book35 = open_workbook('../results/result_htt_v8.9.xls')
book36 = open_workbook('../results/result_htt_v8.10.xls')
book37 = open_workbook('../results/result_htt_v8.11.xls')
# book38 = open_workbook('../results/result_htt_v8.12.xls')
# book39 = open_workbook('../results/result_htt_v8.13.xls')

sheet31 = book31.sheet_by_index(0)
sheet32 = book32.sheet_by_index(0)
sheet33 = book33.sheet_by_index(0)
sheet34 = book34.sheet_by_index(0)
sheet35 = book35.sheet_by_index(0)
sheet36 = book36.sheet_by_index(0)
sheet37 = book37.sheet_by_index(0)
# sheet38 = book38.sheet_by_index(0)
# sheet39 = book39.sheet_by_index(0)

Y3miner = []
Y31, Y32, Y33, Y34, Y35, Y36, Y37, Y38, Y39 = [], [], [], [], [], [], [], [], []
for row_index in xrange(100, 400):
    Y31.append(float(sheet31.cell_value(row_index, column)))
    Y32.append(float(sheet32.cell_value(row_index, column)))
    Y33.append(float(sheet33.cell_value(row_index, column)))
    Y34.append(float(sheet34.cell_value(row_index, column)))
    Y35.append(float(sheet35.cell_value(row_index, column)))
    Y36.append(float(sheet36.cell_value(row_index, column)))
    Y37.append(float(sheet37.cell_value(row_index, column)))
    # Y38.append(float(sheet38.cell_value(row_index, column)))
    # Y39.append(float(sheet39.cell_value(row_index, column)))


Y3miner.append(np.mean(Y31))
Y3miner.append(np.mean(Y32))
Y3miner.append(np.mean(Y33))
Y3miner.append(np.mean(Y34))
Y3miner.append(np.mean(Y35))
Y3miner.append(np.mean(Y36))
Y3miner.append(np.mean(Y37))
# Y3miner.append(np.mean(Y38))
# Y3miner.append(np.mean(Y39))

worksheet.write(1, 2, str(Y3miner[0]))
worksheet.write(2, 2, str(Y3miner[1]))
worksheet.write(3, 2, str(Y3miner[2]))
worksheet.write(4, 2, str(Y3miner[3]))
worksheet.write(5, 2, str(Y3miner[4]))
worksheet.write(6, 2, str(Y3miner[5]))
worksheet.write(7, 2, str(Y3miner[6]))
# worksheet.write(8, 2, str(Y3miner[7]))
# worksheet.write(9, 2, str(Y3miner[8]))

print(Y3miner)

book41 = open_workbook('../results/result_bc_v8.5.xls')
book42 = open_workbook('../results/result_bc_v8.6.xls')
book43 = open_workbook('../results/result_bc_v8.7.xls')
book44 = open_workbook('../results/result_bc_v8.8.xls')
book45 = open_workbook('../results/result_bc_v8.9.xls')
book46 = open_workbook('../results/result_bc_v8.10.xls')
book47 = open_workbook('../results/result_bc_v8.11.xls')
# book48 = open_workbook('../results/result_bc_v8.12.xls')
# book49 = open_workbook('../results/result_bc_v8.13.xls')

sheet41 = book41.sheet_by_index(0)
sheet42 = book42.sheet_by_index(0)
sheet43 = book43.sheet_by_index(0)
sheet44 = book44.sheet_by_index(0)
sheet45 = book45.sheet_by_index(0)
sheet46 = book46.sheet_by_index(0)
sheet47 = book47.sheet_by_index(0)
# sheet48 = book48.sheet_by_index(0)
# sheet49 = book49.sheet_by_index(0)

Y4miner = []
Y41, Y42, Y43, Y44, Y45, Y46, Y47, Y48, Y49 = [], [], [], [], [], [], [], [], []
for row_index in xrange(100, 400):
    Y41.append(float(sheet41.cell_value(row_index, column)))
    Y42.append(float(sheet42.cell_value(row_index, column)))
    Y43.append(float(sheet43.cell_value(row_index, column)))
    Y44.append(float(sheet44.cell_value(row_index, column)))
    Y45.append(float(sheet45.cell_value(row_index, column)))
    Y46.append(float(sheet46.cell_value(row_index, column)))
    Y47.append(float(sheet47.cell_value(row_index, column)))
    # Y48.append(float(sheet48.cell_value(row_index, column)))
    # Y49.append(float(sheet49.cell_value(row_index, column)))

Y4miner.append(np.mean(Y41))
Y4miner.append(np.mean(Y42))
Y4miner.append(np.mean(Y43))
Y4miner.append(np.mean(Y44))
Y4miner.append(np.mean(Y45))
Y4miner.append(np.mean(Y46))
Y4miner.append(np.mean(Y47))
# Y4miner.append(np.mean(Y48))
# Y4miner.append(np.mean(Y49))

worksheet.write(1, 3, str(Y4miner[0]))
worksheet.write(2, 3, str(Y4miner[1]))
worksheet.write(3, 3, str(Y4miner[2]))
worksheet.write(4, 3, str(Y4miner[3]))
worksheet.write(5, 3, str(Y4miner[4]))
worksheet.write(6, 3, str(Y4miner[5]))
worksheet.write(7, 3, str(Y4miner[6]))
# worksheet.write(8, 3, str(Y4miner[7]))
# worksheet.write(9, 3, str(Y4miner[8]))

print(Y4miner)
plt.plot(X, Y1miner, '^-', label="DQN policy", zorder=10)
plt.plot(X, Y2miner, 'o-', label="Random policy", zorder=10)
plt.plot(X, Y3miner, '*-', label="HTT policy", zorder=10)
plt.plot(X, Y4miner, '+-', label="Backscatter policy", zorder=10)


plt.xlabel('Number of busy time slots per time frame')
plt.legend()
plt.show()
workbook.close()