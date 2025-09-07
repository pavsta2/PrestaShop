import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RegistrPage(BasePage):
    MALE_GENDER_CHBX = By.ID, 'field-id_gender-1'
    FNAME_FLD = By.ID, 'field-firstname'
    LNAME_FLD = By.ID, 'field-lastname'
    EMAIL_FLD = By.ID, 'field-email'
    PASS_FLD = By.ID, 'field-password'
    I_AGREE_CHBX = By.XPATH, '*//input[@name ="psgdpr"]'
    CUST_DATA_PRIVACY_CHBX = By.XPATH, '*//input[@name ="customer_privacy"]'
    ERR_MESS = By.XPATH, '*//div[@class="col-md-6 js-input-column"]/div/ul/li'
    SAVE_BTN = By.XPATH, '*//button[@class="btn btn-primary form-control-submit float-xs-right"]'

    def fill_user_form(self,
                       fname,
                       lname,
                       email,
                       password):
        self.logger.info(
            '%s: Clicking checkbox with locator: %s' % (self.class_name, self.MALE_GENDER_CHBX))
        self.click_elem(self.MALE_GENDER_CHBX)
        self.logger.info(
            '%s: Filling first name field with locator: %s' % (self.class_name, self.FNAME_FLD))
        self.fill_the_field(self.FNAME_FLD, fname)
        self.logger.info(
            '%s: Filling last name field with locator: %s' % (self.class_name, self.LNAME_FLD))
        self.fill_the_field(self.LNAME_FLD, lname)
        self.logger.info(
            '%s: Filling email field with locator: %s' % (self.class_name, self.EMAIL_FLD))
        self.fill_the_field(self.EMAIL_FLD, email)
        self.logger.info(
            '%s: Filling password field with locator: %s' % (self.class_name, self.PASS_FLD))
        self.fill_the_field(self.PASS_FLD, password)
        self.logger.info(
            '%s: Clicking checkbox with locator: %s' % (self.class_name, self.I_AGREE_CHBX))
        self.click_elem(self.I_AGREE_CHBX)
        self.logger.info(
            '%s: Clicking checkbox with locator: %s' % (self.class_name, self.CUST_DATA_PRIVACY_CHBX))
        self.click_elem(self.CUST_DATA_PRIVACY_CHBX)