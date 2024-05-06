import xlsxwriter
import asyncio
import database
from sqlalchemy import select


async def make_xlsx(name="meteo_output.xlsx", n=10):
    output_list = []
    with database.Session(autoflush=False, bind=database.engine) as session:

        stmt = select(database.Msg).limit(n)  # получаем последние n записей
        data = session.execute(stmt)

        for item in data:
            output_list.append(item[0].get_list())

    workbook = xlsxwriter.Workbook(name)

    head = ['Температура', 'Направление ветра', 'Скорость ветра', 'Давление', 'Погода', 'Осадки']

    header = workbook.add_format({'bold': True, 'font_size': 11, 'border': True})  # Формат шрифта для шапки
    header.set_text_wrap()
    usual = workbook.add_format({'border': True})  # Формат шрифта для всех остальных записей
    usual.set_text_wrap()

    worksheet = workbook.add_worksheet('Лист1')  # Ширина столбцов
    worksheet.set_column('A:B', 15)
    worksheet.set_column('C:C', 30)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 30)
    worksheet.set_column('F:F', 15)

    row = 0
    for i in range(len(head)):  # Заголовок
        worksheet.write(row, i, head[i], header)
    row += 1

    for item in output_list:
        j = 0
        for j in range(len(item)):
            data_tmp = item[j]
            worksheet.write(row, j, data_tmp, usual)  # Основные записи
        row += 1
    workbook.close()


if __name__ == '__main__':
    asyncio.run(make_xlsx("meteo_output.xlsx", 10))
