from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_TITLE = By.XPATH, '*//h1'
    PROD_NAME_FIELD = By.XPATH, '//*[@id="main"]/div/div[1]/div/div[2]/ul/li/div/div[2]/div[1]/a'
    TOTAL_PRICE = By.XPATH, '*//div[@class="cart-summary-line cart-total"]/span[2]'
