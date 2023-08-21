import requests
import pandas as pd
import utility

# Константы, URL для запроса и API ключ
url = "http://api.weatherapi.com/v1"
apikey = ""
weather_emojis = pd.read_csv('conditions.csv')

'''params = {
        "key": apikey,
        "q": "Moscow",
        'days': 4,
        "lang": "ru"
        }

response = requests.get(url + "/forecast.json", params=params).json()
print(response['forecast']['forecastday'][0]['day']['condition']['icon'])'''


# Возвращает погоду в формате число-время - Погода - темпервтура
def get_weather_for_date(city, day):
    # Вводные параметры для запроса
    params = {
        "key": apikey,
        "q": city,
        'days': 4,
        "lang": "ru"
    }

    # Делаем запрос относительно параметров
    response = requests.get(url + "/forecast.json", params=params).json()
    # Суда записывается сам прогноз
    forecast = ''

    # Цикл проходит,собирает информацию и записывает её в переменную
    for i in range(len(response['forecast']['forecastday'][day]['hour'])):
        condition = response['forecast']['forecastday'][day]['hour'][i]['condition']['text']
        forecast += f"<b>{response['forecast']['forecastday'][day]['hour'][i]['time'][-5:]}</b> - " \
                    f"{condition} {utility.find_in_csv_dict_table(weather_emojis, condition)} - " \
                    f"{response['forecast']['forecastday'][day]['hour'][i]['temp_c']}°C\n"

    return forecast
