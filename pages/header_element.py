import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HeaderElement(BasePage):
    SEARCH_FIELD = By.NAME, "s"
    CART_BTN = By.ID, '_desktop_cart'
    SIGN_IN_BTN = By.XPATH, '*//span[contains(text(), "Sign in")]'
    CURR_DROPDOWN_BTN = By.XPATH, '*//i[@class="material-icons expand-more"]'
    CURR_DROPDOWN = By.XPATH, '*//ul[@aria-labelledby="currency-selector-label"]'
    EUR_OPTION = By.XPATH, '*//a[@title="Euro"]'
    USD_OPTION = By.XPATH, '*//a[@title="US Dollar"]'
    REGISTR_USER = By.XPATH, '*//a[@class="account"]'

    def change_currency(self, curr_usd_or_euro: str):
        self.logger.info('%s: Changing currency on %s' % (self.class_name, curr_usd_or_euro))
        if curr_usd_or_euro == 'usd':
            self.logger.info(
                '%s: Opening currency dropdown with locator: %s' % (self.class_name, self.CURR_DROPDOWN_BTN))
            self.click_elem(self.CURR_DROPDOWN_BTN)
            time.sleep(2)
            self.logger.info(
                '%s: Clicking currency option with locator: %s' % (self.class_name, self.USD_OPTION))
            self.click_elem(self.USD_OPTION)
        else:
            self.logger.info(
                '%s: Opening currency dropdown with locator: %s' % (self.class_name, self.CURR_DROPDOWN_BTN))
            self.click_elem(self.CURR_DROPDOWN_BTN)
            time.sleep(2)
            self.logger.info(
                '%s: Clicking currency option with locator: %s' % (self.class_name, self.EUR_OPTION))
            self.click_elem(self.EUR_OPTION)