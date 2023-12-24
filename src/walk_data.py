# Подключение необходимых библиотек
import requests
import datetime
from src.config import weatherapi_token

# Функция для полчения погоды от weatherapi
def get_weather(city):
    token = weatherapi_token
    response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={token}&q={city}&aqi=no").json()
    weather = {
        'city': response['location']['name'],
        'temp': response['current']['temp_c'],
        'wind': round(response['current']['wind_kph'] * 1000 / 3600, 2),
        'icon': response['current']['condition']['icon']
    }
    return weather

# Функция для полчения совета для прогулки с питомцем на основании классических алгоритмов
def get_walk_advice(weather, pet_data):
    current_date = datetime.datetime.now()
    
    temp_advice = ""
    wind_advice = ""
    temp = weather['temp']
    wind = weather['wind']
    if pet_data:
        weight = pet_data['weight']
        # Формирование совета на основании данных температуры
        if temp <= -20:
            temp_advice = "Категорически рекомендуется одеть утепленный комбинезон или свитер + штаны"
        elif temp > -20 and temp < -10:
            temp_advice = "Рекомендуется одеть утепленный комбинезон с подкладкой"
        elif temp >= -10 and temp < 0:
            temp_advice = "Рекомендуется одеть комбинезон без подкладки"
        elif temp >= 0 and temp < 5:
            if current_date.month in [12, 1, 2]:
                temp_advice = "Обратите внимание, возможны реагенты на асфальте, может понадобиться обувь"
        else: 
            temp_advice = "Температурные рекомендации отсутствуют"
        # Формирование совета на основании данных о ветре и весе питомца
        if wind >= 20 and weight <= 10:
            wind_advice = "Обратите внимание, сильный ветер может навредить вашему питомцу"
        else:
            wind_advice = "Рекомендации на основании данных о ветре отсутствуют"
    walk_advice = {
        'temp_advice': temp_advice,
        'wind_advice': wind_advice
    }
    return walk_advice