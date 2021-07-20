"""
xls (Excel 2003) - import xlrd, xlwt
"""
import xlwt
from io import BytesIO
import datetime
from decimal import Decimal

styleHeader = xlwt.easyxf(
    """font: bold on,name Arial, height 200; borders: left thin,top thin,right thin,bottom thin;
    align: horiz center,vert center""")
style_date = xlwt.easyxf(num_format_str='DD.MM.YYYY')
style_amount = xlwt.easyxf(num_format_str='#,##0.0')
style_default = xlwt.XFStyle()


# col_width = 256 * 15  # 15 characters wide
# headFont.height = 10 * 20  # font size 10


def query_to_excel2003(query_result,
                       sheet_name: str = 'Лист 1',
                       startrow=0,
                       columns={}) -> BytesIO:

    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheet_name)

    columnwidth = {}

    if not columns:  # если поля не заданы - создаем словарь колонок
        columns = {key: key for key in query_result[0].keys()}

    row = startrow

    # добавляем заголовки
    for col_index, col_name in enumerate(columns):
        colomndata = columns.get(col_name)
        # сохраняем ширину колонки
        if col_index in columnwidth:
            if len(colomndata) > columnwidth[col_index]:
                columnwidth[col_index] = len(colomndata)
        else:
            columnwidth[col_index] = len(colomndata)

        ws.write(row, col_index, colomndata, styleHeader)
    # ===================================================

    for item in query_result:
        row += 1
        for col_index, col_name in enumerate(columns):
            colomndata = item.get(col_name)

            # определяем формат поля для вывода
            style = style_default
            if isinstance(colomndata, (datetime.date, datetime.datetime)):
                colomndata = colomndata.strftime(
                    "%d.%m.%Y")  # для расчета ширины колонки
                style = style_date
            elif isinstance(colomndata, Decimal):
                style = style_amount if colomndata > 0 else style_default

            # пишим в файл
            ws.write(row, col_index, colomndata, style)

            # сохраняем ширину колонки
            if col_index in columnwidth:
                if len(str(colomndata)) > columnwidth.get(col_index, 0):
                    columnwidth[col_index] = len(colomndata)
            else:
                columnwidth[col_index] = len(colomndata)

    # устанавливаем ширину колонок
    for column, widthvalue in columnwidth.items():
        ws.col(column).width = (widthvalue + 4) * 256

    f = BytesIO()
    wb.save(f)
    f.seek(0)

    return f
