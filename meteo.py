import sys
import excel
import data_update
import asyncio


async def read_input():

    help_message = 'Доступные команды:\n' \
                   'export/экспорт для формирования xlsx файла. Опционально название файла и количество строк. \n' \
                   'Пример: export file.xlsx 10\n' \
                   '\n' \
                   'exit/выход для остановки программы\n' \
                   '\n' \
                   'help/помощь для вывода этого сообщения\n'

    while True:
        data = await loop.run_in_executor(None, input, "Enter command: ")  # Ожидаем ввод команды

        command = str(data).replace('\n', '').split(' ')  # убираем символ переноса строки и разбиваем команду по пробелам

        if command[0] == 'help' or command[0] == 'помощь':
            print(help_message)
        elif command[0] == 'export' or command[0] == 'экспорт':
            name = "meteo_output.xlsx"
            n = 10
            try:  # Простая конструкция для проверки ввода опциональных параметров
                name = command[1]
            except IndexError:
                pass

            try:
                n = int(command[2])
            except IndexError:
                pass

            await excel.make_xlsx(name, n)
        elif command[0] == 'exit' or command[0] == 'выход':
            sys.exit()  # Завершение программы
        else:
            print('Wrong command. Try again or use help.')


async def main():  # Основная функция, обеспечивающая асинхронность
    task = asyncio.create_task(read_input())

    await data_update.main()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
