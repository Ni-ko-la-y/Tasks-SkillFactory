from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначало получаем API ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets', либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Тайга2', animal_type='Немецкая овчарка', age='3',
                                     pet_photo='images/tayga.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ API и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем, если список своих питомцев пустой, добавляем нового и
    # снова запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Найда', 'немецкая овчарка', '4', 'images/tayga.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Берём id первого питомца из списка, и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем, что статус ответа равен 200, и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name = 'Тайга', animal_type = 'Овчарка', age = 5):
    '''Проверяем возможность обновления информации о питомце'''

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить имя, тип и возраст питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'] [0] ['id'], name, animal_type, age)

        # Проверяем, что статус ответа 200, и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


""" Ещё 10 различных тестов для REST API интерфейса"""


def test_successful_add_new_pet_without_photo(name = 'Найда', animal_type = 'Немецкая овчарка', age = 2):
    """Проверяем возможность добавления питомца без фото"""

    # Запрашиваем ключ API и сохраняем
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_add_photo_of_pet(pet_photo = 'images/nayda.jpg'):
    """Тест на успешное добавление фото питомцу"""

    # Запрашиваем ключ API и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Определяем ID питомца и полный путь к фото:
    pet_id = my_pets ['pets'][0]['id']
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем фото питомца
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Проверяем статус ответа и добавленное фото питомца
    assert status == 200
    assert result.get('pet_photo') != ''
    print(result.get('pet_photo'))


def test_negative_pet_photo_change(pet_photo = 'images/nayda2.gif'):
    """Негативный тест замены фото питомца"""

    # Запрашиваем ключ API и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Определяем ID питомца и полный путь к фото:
    pet_id = my_pets['pets'][0]['id']
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Меняем фото питомца, используя расширение файла .gif
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    # Проверяем, что фото не поменялось
    assert status != 200


def test_get_api_key_for_not_valid_user(email = 'ojo@mail.com', password = '2545'):
    """Проверяем, что запрос API ключа через ложный email не проходит"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем данные
    assert status != 200
    assert 'key' not in result


def test_get_api_key_no_password(email = valid_email, password = ''):
    """Проверка получить ключ API без ввода пароля"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Проверяем результат
    assert  status != 200
    assert 'key' not in result

def test_delete_pet_general_list():
    """Проверяем возможность удалить чужого питомца из общей базы данных"""

    # Получаем ключ auth_key и запрашиваем общий список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, gen_list = pf.get_list_of_pets(auth_key, "")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = gen_list['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем общий список питомцев
    _, gen_list = pf.get_list_of_pets(auth_key, "")

    # Положительный результат обозначит место бага
    assert status == 200
    assert pet_id not in gen_list

    """ Пользователь может удалять чужих питомцев, это - критический баг."""


def test_add_new_pet_with_incorrect_data(name='353@%^&*/(+=46561.303,5153', animal_type='',
                                         age='546450000604640664565464468', pet_photo='images/nayda.jpg'):
    """ Пробуем добавить питомца с некорректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем результат
    assert status == 200
    assert result['age'] == age

    """Тест показал возможность создания объекта с некорректными данными, это - баг"""


def test_update_pet_info_empty_data_my_pets(name=' ', animal_type=' ', age=' '):
    """Пробуем обновить объект в 'Мои питомцы' пустыми данными"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Обновляем данные
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем статус и изменения
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

    """Объект обновляется пустыми значениями - баг"""


def test_update_pet_info_empty_data_general_list(name=' ', animal_type=' ', age=' '):
    """Проверяем возможность обновить объект в общем списке пустыми данными"""

    # Получаем ключ auth_key и общий список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, gen_list = pf.get_list_of_pets(auth_key, "")

    #Обновляем данные
    status, result = pf.update_pet_info(auth_key, gen_list['pets'][0]['id'], name, animal_type, age)

    # Проверяем статус и изменения
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

    """ Данные объекта из общего списка заполняются пустыми значениями - баг"""


def test_update_pet_info_general_list(name='Обновление', animal_type='сервера', age ='1'):
    """Проверяем возможность изменить данные чужого питомца в общем списке"""

    # Получаем ключ auth_key и общий список питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, gen_list = pf.get_list_of_pets(auth_key, "")

    # Пробуем изменить данные
    status, result = pf.update_pet_info(auth_key, gen_list['pets'][0]['id'], name, animal_type, age)

    # Проверяем статус и изменения
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

    """Можно подменить данные в чужом объекте - баг"""

