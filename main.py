import traceback
from typing import NamedTuple, List, Dict

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

password = 'p#Gaf*9aCt4_EW$'
mail = 'somemail@mailforspam.com'

test_page = 'https://www.yaklass.ru/TestWorkRun/Preview/2656450'
auth_page = 'https://www.yaklass.ru/Account/Login'

driver = webdriver.Chrome()


def auth(driver, login, password):
    """
    Переходит на страницу авторизации и вводит данные аккаунта
    :param driver: экземпляр браузера
    :param login: ваш логин в система
    :param password: ваш пароль
    :return:
    """
    driver.get(auth_page)
    name_filed = driver.find_element_by_id('UserName')
    password_field = driver.find_element_by_id('Password')
    login_form = driver.find_element_by_id('loginform')
    approve_buttons = login_form.find_element_by_class_name('btn')

    name_filed.send_keys(login)
    password_field.send_keys(password)

    approve_buttons.click()


def start_test(driver: webdriver.Chrome, page_test: str):
    """
    Переходит на страницу тестирования и начинает тест
    :param driver:
    :param page_test:
    :return:
    """
    driver.get(page_test)
    # TODO проверить работоспособность
    driver.find_element_by_class_name('btn').click()


class TestQuestion(NamedTuple):
    """
    Класс для хранения информации о задании
    """
    # текст вопроса
    question: str
    # перчень вариантов ответа
    variants: List[str]
    type: str = 'с вариантами ответов'


def get_question_content(driver: webdriver.Chrome) -> WebElement:
    """
    Получает часть страницы, содержащую информацию о вопросе
    :param driver: драйвер браузера
    :return:
    """
    return driver.find_element_by_id('taskhtml')


def parse_question(element: WebElement) -> TestQuestion:
    """
    Собирает информацию о вопросе.

    На данный момент эта функция работает только с вопросами, предлагающими варианты ответа.
    Для других типов вопросов необходимо добавить реализации сборщиков
    :param element: веб элемент, содержащий необходимую информацию
    :return:
    """
    # TODO сделать возможность парсинга для других типов вопросов (тут реализован только выбор из варинатов ответов)
    text = element.find_element_by_tag_name('p').text
    variants: List[WebElement] = element.find_element_by_class_name('maxpoints1').find_elements_by_tag_name('li')
    varaints_text: List[str] = [i.text for i in variants]
    # TODO: выбор варианта из variants и клик на него через .click()
    return TestQuestion(text, varaints_text)


def parse_test(driver: webdriver.Chrome, test_url: str) -> List[TestQuestion]:
    """
    Собирает все вопросы с вариантами ответов

    :param driver: драйвер браузера
    :param test_url: адрес страницы с тестов
    :return: список вопросов с ответами
    """
    start_test(driver, test_url)
    questions_count = int(driver.find_element_by_class_name('position').text.split('/')[1])
    questions: List[TestQuestion] = []
    for i in range(questions_count):
        try:
            question_content = get_question_content(driver)
            question = parse_question(question_content)
            questions.append(question)

            driver.find_element_by_class_name('btn').click()
        except Exception as e:
            print('failed to parse question number:', i + 1, 'cause of:', traceback.format_exc())

    print(questions)
    return questions


def parse_answers(driver: webdriver.Chrome) -> Dict[int, str]:
    """
    Собирает ответы для вопросов теста
    :param driver браузер, перешедший на страницу с ответами
    :return:
    """
    # TODO сбор информации о ответах
    pass


auth(driver, mail, password)
parse_test(driver, test_page)
driver.close()
