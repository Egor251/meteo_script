import sys
import excel
import data_update

import asyncio


async def read_input():

    help_message = ''

    while True:
        data = await loop.run_in_executor(None, input, "Enter something: ")

        command = str(data).replace('\n', '').split(' ')

        if command[0] == 'help' or command[0] == 'помощь':
            print(help_message)
        elif command[0] == 'export' or command[0] == 'экспорт':
            name = "meteo_output.xlsx"
            n = 10
            try:
                name = command[1]
            except IndexError:
                pass

            try:
                n = int(command[2])
            except IndexError:
                pass
            await excel.make_xlsx(name, n)
        elif command[0] == 'exit' or command[0] == 'выход':
            sys.exit()
        else:
            print('Wrong command. Try again or use help.')


async def main():
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
