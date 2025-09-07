import requests
import allure


class BaseHTTPMeth:
    def __init__(self, logger):
        self.logger = logger
        self.class_name = type(self).__name__

    @allure.step("Выполнение запроса GET")
    def get_meth(self, url, headers):
        self.logger.debug('Get request with url: %s' % url)
        return requests.get(headers=headers, url=url)

    @allure.step("Выполнение запроса POST")
    def post_meth(self, url, headers, body):
        self.logger.debug('Post request with url: %s' % url)
        return requests.post(url=url, headers=headers, data=body)

    @allure.step("Выполнение запроса PATCH")
    def patch_meth(self, url, headers, body):
        self.logger.debug('Patch request with url: %s' % url)
        return requests.patch(url=url, headers=headers, data=body)