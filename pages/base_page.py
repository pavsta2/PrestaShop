"""Модуль базовых методов взаимодействия с элементами"""
import allure
import random
import string
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    def __init__(self, driver, wait=4):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=wait)
        self.actions = ActionChains(driver)
        self.logger = driver.logger
        self.class_name = type(self).__name__

    @allure.step("Открытие страницы {url}")
    def open(self, url):
        self.driver.get(url)

    @allure.step("Получение объекта элемента {locator}")
    def get_element(self, locator: tuple):
        self.logger.debug('%s: Getting element %s' % (self.class_name, str(locator)))
        try:
            el = self.wait.until(EC.presence_of_element_located(locator),
                             message='No such element')
        except TimeoutException:
            assert False, 'Элемент не найден'
        return el

    @allure.step("Получение списка объектов элементов {locator}")
    def get_elements(self, locator: tuple):
        self.logger.debug('%s: Getting elements %s' % (self.class_name, str(locator)))
        try:
            els = self.wait.until(EC.presence_of_all_elements_located(locator),
                              message='No such element')
        except TimeoutException:
            assert False, 'Элемент не найден'
        return els

    @allure.step("Заполняется поле {locator} данным {test_data}")
    def fill_the_field(self, locator: tuple, test_data: str) -> None:
        el = self.get_element(locator)
        self.logger.debug('%s: Moving to element %s' % (self.class_name, str(locator)))
        self.actions.move_to_element(el).pause(1).click().perform()
        self.logger.debug('%s: Clearing element %s' % (self.class_name, str(locator)))
        el.clear()
        self.logger.debug('%s: Sending keys %s to element %s' % (self.class_name, test_data, str(locator)))
        for i in test_data:
            el.send_keys(i)

    @allure.step("Клик по элементу {locator}")
    def click_elem(self, locator: tuple) -> None:
        el = self.get_element(locator)
        self.logger.debug('%s: Clicking element %s' % (self.class_name, str(locator)))
        self.actions.move_to_element(el).pause(1).click().release().perform()

    @allure.step("Выбор опции селекта {locator} по индексу {index}")
    def select_opt_by_ind(self, locator: tuple, index=0):
        options = Select(self.get_element(locator))
        self.logger.debug('%s: Selecting option by id:%s in element %s' % (self.class_name, index, str(locator)))
        options.select_by_index(index)

    @allure.step("Проверка наличия текста в элементе {locator}")
    def check_text_in_elem(self, locator: tuple, text: str):
        self.logger.debug('%s: Checking text (%s) presented in element %s' % (self.class_name, text, str(locator)))
        try:
            self.wait.until(EC.text_to_be_present_in_element(locator, text),
                        message='No such text in element')
        except NoSuchElementException:
            assert False, 'Элемент не найден'
        return text

    @allure.step("Поиск элемента, содержащего текст {text}")
    def search_for_elem_contains_text(self, text: str):
        self.get_element((By.XPATH, f"//*[contains(text(), '{text}')]"))

    @allure.step("Генерация рандомных тестовых данных")
    def generate_random_string(length: int) -> str:
        return ''.join(random.choices(string.ascii_letters, k=length))
