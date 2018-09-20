import matplotlib.pyplot as plt
from xlrd import open_workbook
import xlsxwriter
import numpy as np

interval = 10
book = open_workbook('../results/result_v7.0_4channels_600.xls')
book2 = open_workbook('../results/result_v3.0_10_D3QN_04.xls')
book3 = open_workbook('../results/result_v3.0_10_D3QN_06.xls')
book4 = open_workbook('../results/result_v3.0_10_D3QN_08.xls')
book5 = open_workbook('../results/result_v3.0_10_D3QN_10.xls')

book21 = open_workbook('../results/result_v3.0_20_D3QN_02.xls')
book22 = open_workbook('../results/result_v3.0_20_D3QN_04.xls')
book23 = open_workbook('../results/result_v3.0_20_D3QN_06.xls')
book24 = open_workbook('../results/result_v3.0_20_D3QN_08.xls')
book25 = open_workbook('../results/result_v3.0_20_D3QN_10.xls')

book31 = open_workbook('../results/result_v3.0_30_D3QN_02.xls')
book32 = open_workbook('../results/result_v3.0_30_D3QN_04.xls')
book33 = open_workbook('../results/result_v3.0_30_D3QN_06.xls')
book34 = open_workbook('../results/result_v3.0_30_D3QN_08.xls')
book35 = open_workbook('../results/result_v3.0_30_D3QN_10.xls')

file_name = '../result_draw/result_v3.0.xlsx'
workbook = xlsxwriter.Workbook(file_name)
worksheet = workbook.add_worksheet()

sheet = book.sheet_by_index(0)
sheet2 = book2.sheet_by_index(0)
sheet3 = book3.sheet_by_index(0)
sheet4 = book4.sheet_by_index(0)
sheet5 = book5.sheet_by_index(0)

sheet21 = book21.sheet_by_index(0)
sheet22 = book22.sheet_by_index(0)
sheet23 = book23.sheet_by_index(0)
sheet24 = book24.sheet_by_index(0)
sheet25 = book25.sheet_by_index(0)

sheet31 = book31.sheet_by_index(0)
sheet32 = book32.sheet_by_index(0)
sheet33 = book33.sheet_by_index(0)
sheet34 = book34.sheet_by_index(0)
sheet35 = book35.sheet_by_index(0)

length = 1000
start = 3000
end = start + length

X, Y1miner, Y2miner, Y3miner = [], [], [], []
Y11, Y12, Y13, Y14, Y15 = [], [], [], [], []
Y21, Y22, Y23, Y24, Y25 = [], [], [], [], []
Y31, Y32, Y33, Y34, Y35 = [], [], [], [], []
for row_index in xrange(start, end):
    Y11.append(float(sheet.cell_value(row_index, 1)))
    Y12.append(float(sheet2.cell_value(row_index, 1)))
    Y13.append(float(sheet3.cell_value(row_index, 1)))
    Y14.append(float(sheet4.cell_value(row_index, 1)))
    Y15.append(float(sheet5.cell_value(row_index, 1)))

    Y21.append(float(sheet21.cell_value(row_index, 1)))
    Y22.append(float(sheet22.cell_value(row_index, 1)))
    Y23.append(float(sheet23.cell_value(row_index, 1)))
    Y24.append(float(sheet24.cell_value(row_index, 1)))
    Y25.append(float(sheet25.cell_value(row_index, 1)))

    Y31.append(float(sheet31.cell_value(row_index, 1)))
    Y32.append(float(sheet32.cell_value(row_index, 1)))
    Y33.append(float(sheet33.cell_value(row_index, 1)))
    Y34.append(float(sheet34.cell_value(row_index, 1)))
    Y35.append(float(sheet35.cell_value(row_index, 1)))


Y1miner.append(np.mean(Y11))
Y1miner.append(np.mean(Y12))
Y1miner.append(np.mean(Y13))
Y1miner.append(np.mean(Y14))
Y1miner.append(np.mean(Y15))

Y2miner.append(np.mean(Y21))
Y2miner.append(np.mean(Y22))
Y2miner.append(np.mean(Y23))
Y2miner.append(np.mean(Y24))
Y2miner.append(np.mean(Y25))

Y3miner.append(np.mean(Y31))
Y3miner.append(np.mean(Y32))
Y3miner.append(np.mean(Y33))
Y3miner.append(np.mean(Y34))
Y3miner.append(np.mean(Y35))

worksheet.write(1, 0, str(Y1miner[0]))
worksheet.write(1, 1, str(Y2miner[0]))
worksheet.write(1, 2, str(Y3miner[0]))
worksheet.write(2, 0, str(Y1miner[1]))
worksheet.write(2, 1, str(Y2miner[1]))
worksheet.write(2, 2, str(Y3miner[1]))
worksheet.write(3, 0, str(Y1miner[2]))
worksheet.write(3, 1, str(Y2miner[2]))
worksheet.write(3, 2, str(Y3miner[2]))
worksheet.write(4, 0, str(Y1miner[3]))
worksheet.write(4, 1, str(Y2miner[3]))
worksheet.write(4, 2, str(Y3miner[3]))
worksheet.write(5, 0, str(Y1miner[4]))
worksheet.write(5, 1, str(Y2miner[4]))
worksheet.write(5, 2, str(Y3miner[4]))
workbook.close()

print(Y1miner)
print(Y2miner)
X = [0.2, 0.4, 0.6,0.8, 1.0]
plt.xlabel('Number of miners')
plt.plot(X, Y1miner, 'ro-', label="[0;1]", zorder=10)
plt.plot(X, Y2miner, 'bx-', label="[0;2]", zorder=10)
plt.plot(X, Y3miner, 'g*-', label="[0;3]", zorder=10)
# plt.plot(X, Y1miner, 'r', zorder=10)
# plt.plot(X, Y2miner, 'b', zorder=10)
# plt.plot(X, Y3miner, 'g', zorder=10)
plt.legend()
plt.show()