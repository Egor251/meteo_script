from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Cтрока подключения
sqlite_database = "sqlite:///main.db"

engine = create_engine(sqlite_database)  # создаем движок SqlAlchemy

# Раскоментировать для использования postgres
# postgres_database = "postgresql+psycopg2://admin:password@localhost/db"
# engine = create_engine(postgres_database)

# создаем класс сессии
Session = sessionmaker(autoflush=False, bind=engine)


# создаем базовый класс для моделей
class Base(DeclarativeBase):
    pass


# создаем модель, объекты которой будут храниться в бд
class Msg(Base):
    __tablename__ = "main"
    id = Column(Integer, primary_key=True)
    temperature = Column(Float)  # Температура
    wind_speed = Column(Float)  # Скорость ветра
    wind_direction = Column(String)  # Направление ветра
    weather = Column(String)  # Погода
    precipitation = Column(Float)  # осадки
    pressure = Column(Float)  # Давление

    def get_list(self):  # Формируем список для удобного заполнение xlsx файла
        return [self.temperature, self.wind_direction, self.wind_speed, self.pressure, self.weather, self.precipitation]


# создаем таблицы
Base.metadata.create_all(bind=engine)

print("База данных и таблица созданы")


if __name__ == "__main__":
    pass
