import database
from sqlalchemy import insert
import meteo_req
import asyncio


async def main():  # Функция для обновления базы
    while True:
        res = await asyncio.gather(meteo_req.get_data())
        with database.Session(autoflush=False, bind=database.engine) as session:
            request = insert(database.Msg).values(res)
            session.execute(request)
            session.commit()
        await asyncio.sleep(180)  # Период обновления базы в секундах


if __name__ == '__main__':
    asyncio.run(main())
