from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# https://metanit.com/python/database/3.3.php

# строка подключения
sqlite_database = "sqlite:///main.db"
#postgres_database = "postgresql+psycopg2://admin:password@localhost/db1"

# создаем движок SqlAlchemy
engine = create_engine(sqlite_database)
#engine = create_engine(postgres_database)

# создаем класс сессии
Session = sessionmaker(autoflush=False, bind=engine)
# создаем саму сессию базы данных
with Session(autoflush=False, bind=engine) as session:
    pass


# создаем базовый класс для моделей
class Base(DeclarativeBase):
    pass


# создаем модель, объекты которой будут храниться в бд
class Msg(Base):
    __tablename__ = "main"
    id = Column(Integer, primary_key=True)
    temperature = Column(Float)
    wind_speed = Column(Float)
    wind_direction = Column(String)
    weather = Column(String)
    precipitation = Column(Float)
    pressure = Column(Float)

    def get_list(self):
        return [self.temperature, self.wind_direction, self.wind_speed, self.pressure, self.weather, self.precipitation]


# создаем таблицы
Base.metadata.create_all(bind=engine)

print("База данных и таблица созданы")


if __name__ == "__main__":
    pass
