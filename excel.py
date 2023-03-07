# import xlsxwriter
#
#
# workbook = xlsxwriter.Workbook('kongxxi.xlsx')
# worksheet = workbook.add_worksheet()
#
#
# ItemStyle = workbook.add_format({
#         'font_size': 10,
#         'bold': True,
#         # 'bg_color': '#101010',
#         # 'font_color': '#FEFEFE',
#         'align': 'center',
#         'top': 2,
#         'left': 2,
#         'right': 2,
#         'bottom': 2
# })
#
#
# worksheet.write('I4', '29%')
# workbook.close()

# import pandas as pd
#
# ecxelpath = 'biao/kongxxi.xlsx'
# data = pd.read_excel(ecxelpath)
# data.insert(9, 4, '1')
# # data.ix[8][3] = '1'
# data.to_excel(ecxelpath, index=None)

import xlrd
from xlutils.filter import process, XLRDReader, XLWTWriter
ecxelpath = 'biao/test.xls'
workbook = xlrd.open_workbook(ecxelpath, formatting_info=True)
w = XLWTWriter()
# process进行xlrd与xlwt间操作，复制一份。
process(XLRDReader(workbook, 'unknown.xls'), w)
# w.output[0][1]为copy后返回的对象
wb = w.output[0][1]
# style_list为原文件的单元格格式信息，列表对象
style_list = w.style_list

for n, sheet in enumerate(workbook.sheets()):
    sheet2 = wb.get_sheet(n)
    for r in range(sheet.nrows):
        for c, cell in enumerate(sheet.row_values(r)):
            # 若循环到第一个sheet的（3,6）单元格，修改值为2020
            if n == 0 and r == 3 and c == 8:
                values = '21'
            else:
                values = sheet.cell_value(r, c)
            style = style_list[sheet.cell_xf_index(r, c)]
            sheet2.write(r, c, values, style)

wb.save('biao/test1.xls')