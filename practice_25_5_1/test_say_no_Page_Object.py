import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    with webdriver.Chrome('C:/driver/chromedriver.exe') as driver:
        # Переход на страницу авторизации
        driver.get('http://petfriends.skillfactory.ru/login')
        WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))
        # Вводим email
        driver.find_element_by_id('email').send_keys('ok@mail.ru')
        # Вводим пароль
        driver.find_element_by_id('pass').send_keys('12345')
        # Нажимаем кнопку входа в аккаунт
        driver.find_element_by_css_selector('button[type="submit"]').click()
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.card-deck')))

        yield driver

        driver.quit()


def test_show_my_pets(testing):
    driver = testing
    driver.implicitly_wait(5)
    # Переход на страницу "Мои питомцы"
    driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

    # Общее количество питомцев
    number = driver.find_element(By.CLASS_NAME, 'left').text.split("\n")
    number = int((number[1].split(":"))[1])
    # Карточки питомцев
    pet = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
    # Фото
    pet_photo = driver.find_elements(By.CSS_SELECTOR, 'th[scope="row"] img')
    # Кличка
    pet_name = driver.find_elements(By.CSS_SELECTOR, 'td:nth-child(2)')
    # Порода
    pet_bread = driver.find_elements(By.CSS_SELECTOR, 'td:nth-child(3)')
    # Возраст
    pet_age = driver.find_elements(By.CSS_SELECTOR, 'td:nth-child(4)')

    # База питомцев, массив имён и счётчик фото
    pet_data = list()
    name_data = list()
    images = 0

    """----------------- Проверки -------------------"""

    # Присутствуют все питомцы?
    assert len(pet) == number

    # У всех питомцев есть кличка, возраст и порода?
    for i in range(len(pet)):
        assert pet_name[i].text != ''
        assert pet_bread[i].text != ''
        assert pet_age[i].text != ''

        name_data.append(pet_name[i].text)
        pet_data.append([pet_name[i].text, pet_bread[i].text, pet_age[i].text])
        if pet_photo[i].get_attribute('src') != '':
            images += 1

    # Хотя бы у половины питомцев есть фото?
    assert images >= (len(pet_photo)) / 2

    # У всех питомцев разные клички?
    # В списке нет повторяющихся питомцев?
    for i in range(len(pet)):
        name_count = name_data.count(name_data[i])
        pet_count = pet_data.count(pet_data[i])

        assert name_count == 1
        assert pet_count == 1
