from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
import markdown2
from pymongo.errors import ServerSelectionTimeoutError
from src.sample_data import *

app = Flask(__name__)
bootstrap = Bootstrap(app)

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

with open('README.md', 'r', encoding='utf-8') as file:
    readme_content = file.read()
    readme_html = markdown2.markdown(readme_content)

@app.route('/')
def index():
    return render_template('index.html', readme_content=readme_html)

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


    if request.method == 'POST':
        # Обработка редактирования данных
        pet = pets_collection.find_one()
        pet['name'] = request.form['name']
        pet['weight'] = request.form['weight']
        pet['height'] = request.form['height']
        pet['passport_number'] = request.form['passport_number']
        pet['chip_number'] = request.form['chip_number']
        pet['illnesses'] = request.form['illnesses'].split(', ')
        pet['medical_record_link'] = request.form['medical_record_link']
        pets_collection.update_one({'passport_number': passport_number}, {'$set': request.form})

    return render_template('pet_profile.html', pet_data=pet_data)

# О нас
@app.route('/about')
def about():
    # Добавьте свои данные
    about_data = {
        'author_name': 'Your Name',
        'telegram_link': 'https://t.me/e_znova',
        'github_link': 'https://github.com/eznova/petadvicer_proto'
    }
    return render_template('about.html', **about_data)

# О проекте
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

@app.route('/dummy/<dummy_message>')
def dummy(dummy_message):
    return render_template('dummy.html', dummy_message=dummy_message)

if __name__ == '__main__':
    app.run(debug=True)
