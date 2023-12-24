# Подключение необходимых библиотек
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
import markdown2
from pymongo.errors import ServerSelectionTimeoutError
from src.sample_data import *
from src.walk_data import *
from src.gpt import generate_advice
from flask_ngrok import run_with_ngrok
from src.config import ngrok_mode


# Инициализация приложения и его оформления
app = Flask(__name__)
bootstrap = Bootstrap(app)
if ngrok_mode:
    run_with_ngrok(app)

try:
    # Попытка подключения к MongoDB
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    db = client['pets_database']
    pets_collection = db['pets']
except ServerSelectionTimeoutError:
    # Обработка ошибки подключения к MongoDB
    print("Failed to connect to MongoDB. Make sure MongoDB is running.")
    db = None

# Модель данных
class Pet:
    def __init__(self, data):
        self.data = data

# Чтение файла Readme.md для вывода на главную страницу
with open('README.md', 'r', encoding='utf-8') as file:
    readme_content = file.read()
    readme_html = markdown2.markdown(readme_content)
# Генерация совета от нейросети. Функция хранится в src/gpt.py
neuro_advice = generate_advice()

# Метод для отображения главной страницы
@app.route('/')
def index():
    return render_template('index.html', readme_content=readme_html)

# Метод для отображения личного кабинета питомца
@app.route('/pet_profile', methods=['GET', 'POST'])
def pet_profile():
    try:
        # Попытка получения данных из базы данных MongoDB
        passport_number = request.args.get('passport_number')
        pet_data = pets_collection.find_one({'passport_number': passport_number})
    except ServerSelectionTimeoutError:
        # Обработка ошибки подключения к MongoDB
        error_message = "Ошибка подключения к БД. Проверьте, что БД запущена или обратитесь к администратору"
        return render_template('errors.html', error_message=error_message)

    weather = get_weather('Saint-Petersburg')
    walk_advice = get_walk_advice(weather, pet_data)
    if request.method == 'POST':
        return render_template('dummy.html', dummy_message="Вызов формы для редактирования данных питомца")
    else:
        return render_template('pet_profile.html', pet_data=pet_data, weather=weather, walk_advice=walk_advice, neuro_advice=neuro_advice)

# Метод для отображения информации о проекте и авторе
@app.route('/about')
def about():
    about_data = {
        'author_name': 'Elizabeth Znova',
        'telegram_link': 'https://t.me/e_znova',
        'github_link': 'https://github.com/eznova/petadvicer_proto'
    }
    return render_template('about.html', **about_data)

# Метод для отображения служебной страницы для управления определенными функциями через WEB
@app.route('/service')
def service():
    return render_template('service.html')

# Служебный метод API на случай, если база создана, но не была настроена, а в консоли это делать лень
@app.route('/fill_database')
def fill_database():
    try:
        # Заполнение базы данных на основе данных о питомце
        pets_collection.insert_many(sample_pet_data)
        # pets_collection.update_one({}, {'$set': sample_pet_data}, upsert=True)
    except ServerSelectionTimeoutError:
        # Обработка ошибки подключения к MongoDB
        error_message = "Ошибка подключения к БД. Проверьте, что БД запущена или обратитесь к администратору"
        return render_template('errors.html', error_message=error_message)

    return redirect(url_for('pet_profile'))

# Метод для отображения нереализованных функций/обращений к API в виде страницы-заглушки
@app.route('/dummy/<dummy_message>', methods=['GET', 'POST'])
def dummy(dummy_message):
    return render_template('dummy.html', dummy_message=dummy_message)
# Запуск приложения
if __name__ == '__main__':
    if ngrok_mode:
        app.run()
    else:
        app.run(debug=True)