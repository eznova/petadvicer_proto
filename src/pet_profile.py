from app import pets_collection, ServerSelectionTimeoutError, render_template, request

def pet_profile():
    try:
        # Попытка получения данных из базы данных MongoDB
        pet_data = pets_collection.find_one()
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
        pets_collection.update_one({}, {'$set': pet})

    return render_template('pet_profile.html', pet_data=pet_data)