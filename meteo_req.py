import openmeteo_requests
import asyncio
from openmeteo_sdk.Variable import Variable


def wind_d(degrees):  # Функция преобразующая градусы в направление ветра
    winddirections = ("северный", "северо-восточный", "восточный", "юго-восточный", "южный", "юго-западный", "западный",
                      "северо-западный")
    direction = int((degrees + 22.5) // 45 % 8)
    return winddirections[direction]


async def get_data():

    # словарь для преобразования weather code в погоду
    weather = {
        0: 'Чистое небо', 1: 'Небольшая облачность', 2: 'Частичная облачность', 3: 'Облачность', 45: 'Туман',
        46: 'Иней', 51: 'Слабая морось', 53: 'Средняя морось', 55: 'Сильная морось', 56: 'Слабая ледяная морось',
        57: 'Сильная ледяная морось', 61: 'Слабый дождь', 63: 'Дождь', 65: 'Сильный дождь',
        66: 'Слабый ледяной дождь', 67: 'Сильный ледяной дождь', 71: 'Слабый снегопад', 73: 'Снегопад',
        75: 'Сильный снегопад', 77: 'Град', 80: 'Ливень', 81: 'Ливень', 82: 'Ливень', 85: 'Метель',
        86: 'Сильная метель', 95: 'Гроза', 96: 'Гроза и ливень'
    }

    om = openmeteo_requests.Client()
    params = {
        "latitude": 55.7050526657622,
        "longitude": 37.3734477499931,
        "current": ["temperature_2m", 'wind_speed_10m', 'wind_direction_10m', 'weather_code', 'precipitation', 'pressure_msl']
    }

    responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
    response = responses[0]

    # Вытаскиваем данные из ответа сервера
    current = response.Current()
    current_variables = list(map(lambda i: current.Variables(i), range(0, current.VariablesLength())))

    current_temperature_2m = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2, current_variables)).Value()  # Температура
    current_wind_speed = next(filter(lambda x: x.Variable() == Variable.wind_speed and x.Altitude() == 10, current_variables)).Value()  # Скорость ветра
    current_wind_direction = next(filter(lambda x: x.Variable() == Variable.wind_direction and x.Altitude() == 10, current_variables)).Value()  # Направление ветра
    current_wind_direction = wind_d(current_wind_direction)
    current_weather_code = next(filter(lambda x: x.Variable() == Variable.weather_code, current_variables)).Value()  # Погода
    current_precipitation = next(filter(lambda x: x.Variable() == Variable.precipitation, current_variables)).Value()  # Осадки (в мм)
    current_pressure_msl = next(filter(lambda x: x.Variable() == Variable.pressure_msl, current_variables)).Value()*0.750062  # Давление над уровнем моря

    output = dict(temperature=current_temperature_2m, wind_direction=current_wind_direction, wind_speed=current_wind_speed,
                  pressure=current_pressure_msl, weather=weather[current_weather_code], precipitation=current_precipitation)  # формируем словарь для передачи в бд
    return output


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(asyncio.gather(get_data()))[0]
    print(res)
