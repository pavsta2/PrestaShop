"""Модуль фикстур"""
import pytest
import logging
import datetime
from selenium import webdriver
import allure
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FFOptions


def pytest_addoption(parser):
    """Pytest hook для добавления кастомных параметров командной строки"""
    parser.addoption("--api_key", action="store", help="api_key")
    parser.addoption('--browser', default="chrome", help="Which browser to open")
    parser.addoption("--app_url", default='10.0.2.15:8081', help='App base url')
    parser.addoption("--driver_storage", default='/Users/darinastarshinova/yandexdriver', help='Ya driver storage')
    parser.addoption("--headless", action='store_true', help='Headless mode')
    # parser.addoption('--log_level', action='store', default='INFO')
    parser.addoption('--remote_start', action='store_true', help='Remote start')
    parser.addoption('--browser_ver', help='Browser version')
    parser.addoption('--remote_url', default='http://127.0.0.1:8080/wd/hub', help='Remote selenoid server url')


@pytest.fixture
def get_api_key(request):
    """Фикстура получения api_key из pytest_addoption"""
    return request.config.getoption('--api_key')


@pytest.fixture(scope='session')
def logger(request):
    log_level = request.config.getoption('--log_level')
    logger = logging.getLogger(request.node.name)
    logfile_handler = logging.FileHandler(f'Logs/{request.node.name}.log')
    logfile_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s %(asctime)s'))
    logger.addHandler(logfile_handler)
    logger.setLevel(log_level)
    return logger


@pytest.fixture()
def browser(request, logger):
    driver = None
    driver_storage = request.config.getoption('--driver_storage')
    browser_type = request.config.getoption('--browser')
    headless = request.config.getoption('--headless')
    log_level = request.config.getoption('--log_level')
    remote = request.config.getoption('--remote_start')
    browser_ver = request.config.getoption('--browser_ver')
    remote_url = request.config.getoption('--remote_url')

    logger.info('Test is started at %s' % datetime.datetime.now())

    if browser_type == 'chrome':
        if remote:
            options = ChromeOptions()
            options.browser_version = browser_ver
            options.set_capability("selenoid:options", {"enableVNC": True})
            if headless:
                options.add_argument("headless=new")
            driver = webdriver.Remote(command_executor=remote_url, options=options)
        else:
            options = ChromeOptions()
            if headless:
                options.add_argument("headless=new")
            driver = webdriver.Chrome(options=options)
    elif browser_type == 'Yandex':
        options = ChromiumOptions()
        if headless:
            options.add_argument("headless=new")
        driver = webdriver.Chrome(
            options=options,
            service=ChromiumService(executable_path=f'{driver_storage}/yandexdriver')
        )
    elif browser_type == 'Firefox':
        options = FFOptions()
        if headless:
            options.add_argument("headless=new")
        driver = webdriver.Firefox(options=options)

    driver.log_level = log_level
    driver.logger = logger
    driver.test_name = request.node.name
    logger.info('Browser %s started for test %s' % (browser_type, request.node.name))

    request.node.driver = driver
    yield driver
    logger.info('Test is finished at %s' % datetime.datetime.now())

    driver.quit()
