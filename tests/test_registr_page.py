"""Модуль проверок страницы регистрации"""
import allure
import pytest
from pages.registr_page import RegistrPage
from pages.header_element import HeaderElement
from pages.base_page import BasePage


@allure.feature("Проверки страницы регистрации")
class TestRegistrPage:
    """Проверки регистрации нового юзера"""

    @allure.title("Позитивная проверка регистрации юзера")
    @pytest.mark.parametrize('fname, lname, email, passd',
                             [(f'{BasePage.generate_random_string(10)}',
                               f'{BasePage.generate_random_string(10)}',
                               f'{BasePage.generate_random_string(4)}@{BasePage.generate_random_string(4)}.ru',
                               f'{BasePage.generate_random_string(40)}')
                              ],
                             ids=['valid values'])
    def test_reg_user_posit(self, browser, fname, lname, email, passd, get_registr_url):
        """Позитивная проверка регистрации юзера"""
        RegistrPage(browser).open(get_registr_url)
        RegistrPage(browser).fill_user_form(fname, lname, email, passd)
        RegistrPage(browser).click_elem(RegistrPage.SAVE_BTN)
        el = HeaderElement(browser).get_element(HeaderElement.REGISTR_USER)

        assert el.text == f'{fname} {lname}'

    @allure.title("Негативные проверки регистрации юзера")
    @pytest.mark.parametrize('fname, lname, email, passd',
                             [('123456',
                               f'{BasePage.generate_random_string(10)}',
                               f'{BasePage.generate_random_string(4)}@{BasePage.generate_random_string(4)}.ru',
                               f'{BasePage.generate_random_string(40)}'),
                              (f'{BasePage.generate_random_string(10)}',
                               '123456',
                               f'{BasePage.generate_random_string(4)}@{BasePage.generate_random_string(4)}.ru',
                               f'{BasePage.generate_random_string(40)}')
                              ],
                             ids=['Invalid Fname',
                                  'Invalid Lname'
                                  ])
    def test_reg_user_negot(self, browser, fname, lname, email, passd, get_registr_url):
        """Позитивная проверка регистрации юзера"""
        RegistrPage(browser).open(get_registr_url)
        RegistrPage(browser).fill_user_form(fname, lname, email, passd)
        RegistrPage(browser).click_elem(RegistrPage.SAVE_BTN)
        el = RegistrPage(browser).get_element(RegistrPage.ERR_MESS)

        assert el.text == 'Invalid format.'
