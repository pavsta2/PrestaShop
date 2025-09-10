"""Модуль проверок наличия элементов на главной странице"""
import allure
from pages.main_page import MainPage
from pages.cart_page import CartPage
from pages.header_element import HeaderElement


@allure.feature("Проверки главной страницы")
class TestMainPage:
    """Проверки главной страницы"""

    @allure.title("Проверка заголовка окна главной страницы")
    def test_window_title(self, browser, get_base_url):
        """Проверка заголовка окна главной страницы"""
        MainPage(browser).open(get_base_url)
        assert browser.title == 'PrestaShop'

    @allure.title("Проверка наличия поискового поля и текста плейсхолдера в нем")
    def test_search_field(self, browser, get_base_url):
        """Проверка наличия поискового поля и текста плейсхолдера в нем"""
        MainPage(browser).open(get_base_url)
        el = HeaderElement(browser).get_element(HeaderElement.SEARCH_FIELD)
        assert el.get_attribute('placeholder') == 'Search our catalog 1'

    @allure.title("Проверка наличия блока кнопки корзины")
    def test_cart_btn(self, browser, get_base_url):
        """Проверка наличия блока кнопки корзины"""
        MainPage(browser).open(get_base_url)
        el = HeaderElement(browser).get_element(HeaderElement.CART_BTN)
        assert el.text.split(' ')[1] == 'Cart'

    @allure.title("Проверка помещения товара в корзину")
    def test_add_prod_to_cart(self, browser, get_base_url):
        """Проверка помещения товара в корзину"""
        MainPage(browser).open(get_base_url)
        MainPage(browser).put_first_card_prod_in_cart()
        el = MainPage(browser).get_element(MainPage.ADD_TO_CART_MSG)
        assert el.text == 'Product successfully added to your shopping cart'

    @allure.title("Проверка невозможности перехода на страницу корзины без добавления товара")
    def test_move_to_cart_page_negot(self, browser, get_base_url):
        """Проверка невозможности перехода на страницу корзины без добавления товара"""
        MainPage(browser).open(get_base_url)
        HeaderElement(browser).click_elem(HeaderElement.CART_BTN)
        el = CartPage(browser).get_element(CartPage.CART_TITLE)
        assert el.text == ''

    @allure.title("Проверка перехода на страницу корзины после добавления товара")
    def test_move_to_cart_page_posit(self, browser, get_base_url):
        """Проверка перехода на страницу корзины после добавления товара"""
        MainPage(browser).open(get_base_url)
        prod_name_in_card = MainPage(browser).get_element(MainPage.FIRST_PROD_CARD_TEXT).text
        MainPage(browser).put_first_card_prod_in_cart()
        MainPage(browser).get_element(MainPage.ADD_TO_CART_MSG)
        MainPage(browser).open(get_base_url)
        HeaderElement(browser).click_elem(HeaderElement.CART_BTN)
        el_title = CartPage(browser).get_element(CartPage.CART_TITLE)
        prod_name_in_cart = CartPage(browser).get_element(CartPage.PROD_NAME_FIELD)
        assert el_title.text == 'SHOPPING CART'
        assert prod_name_in_cart.text.lower() == prod_name_in_card.lower()
