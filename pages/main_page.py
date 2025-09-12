from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MainPage(BasePage):
    FIRST_PROD_CARD = By.XPATH, '//*[@id="content"]/section[1]/div/div[1]/article/div/div[1]/a'
    FIRST_PROD_CARD_TEXT = By.XPATH, '//*[@id="content"]/section[1]/div/div[1]/article/div/div[2]/h3/a'
    BTN_CART_IN_CARD = By.XPATH, '//*[@id="add-to-cart-or-refresh"]/div[2]/div[1]/div[2]/button'
    ADD_TO_CART_MSG = By.ID, 'myModalLabel'

    def put_first_card_prod_in_cart(self):
        self.logger.info('%s: Put product from first card into cart' % self.class_name)
        self.click_elem(self.FIRST_PROD_CARD)
        self.click_elem(self.BTN_CART_IN_CARD)
