"""Модуль проверок на странице корзины"""
import allure
from pages.main_page import MainPage
from pages.cart_page import CartPage
from pages.header_element import HeaderElement


@allure.feature("Проверки главной страницы")
class TestCartPage:
    """Проверки страницы корзины"""

    @allure.title("Проверка установки валюты USD в корзине")
    def test_change_curr_to_usd(self, browser, get_base_url, get_cart_url):
        """Проверка изменения валюты в корзине"""
        MainPage(browser).open(get_base_url)
        MainPage(browser).put_first_card_prod_in_cart()
        MainPage(browser).get_element(MainPage.ADD_TO_CART_MSG)

        CartPage(browser).open(get_cart_url)
        HeaderElement(browser).change_currency('usd')
        total_price_el = CartPage(browser).get_element(CartPage.TOTAL_PRICE)
        assert total_price_el.text[0] == '$'

    @allure.title("Проверка установки валюты EURO в корзине")
    def test_change_curr_to_euro(self, browser, get_base_url, get_cart_url):
        """Проверка изменения валюты в корзине"""
        MainPage(browser).open(get_base_url)
        MainPage(browser).put_first_card_prod_in_cart()
        MainPage(browser).get_element(MainPage.ADD_TO_CART_MSG)

        CartPage(browser).open(get_cart_url)
        HeaderElement(browser).change_currency('euro')
        total_price_el = CartPage(browser).get_element(CartPage.TOTAL_PRICE)
        assert total_price_el.text[0] == '€'
