import allure
from .base_http_methods import BaseHTTPMeth


class ApiRequest(BaseHTTPMeth):
    """Класс, описывающий методы Presta Api"""
    @allure.step("Выполнение запроса получения товара по id")
    def get_product(self, api_key, prod_id):
        url = f'http://localhost:8082/api/products/{prod_id}'
        headers = {
            'Output-Format': 'JSON',
            'Authorization': f'{api_key}',
            'Content-Type': 'text/plain'
        }
        self.logger.info(
            '%s: Making GET request for product with id: %s' % (self.class_name, prod_id))
        return self.get_meth(url, headers)

    @allure.step("Выполнение запроса списка всех товаров")
    def get_products(self, api_key):
        url = f'http://localhost:8082/api/products'
        headers = {
            'Output-Format': 'JSON',
            'Authorization': f'{api_key}',
        }
        self.logger.info(
            '%s: Making GET request for list of all products' % self.class_name)
        return self.get_meth(url, headers)

    @allure.step("Получение максимального id товара")
    def get_product_max_id(self, api_key):
        url = f'http://localhost:8082/api/products'
        headers = {
            'Output-Format': 'JSON',
            'Authorization': f'{api_key}',
        }
        self.logger.info(
            '%s: Making GET request for list of all products and getting last(max) id' % self.class_name)
        return self.get_meth(url, headers).json()['products'][-1]['id']

    @allure.step("Выполнение запроса создания производителя")
    def create_manufacture(self, api_key, manufacture_name):
        url = "http://localhost:8082/api/manufacturers"

        payload = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                   "<prestashop xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n"
                   "    <manufacturer>\n"
                   f"        <name>{manufacture_name}</name>\n"
                   "    </manufacturer>\n"
                   "</prestashop>")
        headers = {
            'Output-Format': 'JSON',
            'Content-Type': 'application/xml',
            'Authorization': f'{api_key}'
        }
        self.logger.info(
            '%s: Making POST request for creating manufacturer with name: %s' % (self.class_name, manufacture_name))
        resp = self.post_meth(url, headers, payload)

        return resp

    @allure.step("Выполнение запроса получения производителя по id")
    def get_manufacture_by_id(self, api_key, manuf_id):
        url = f'http://localhost:8082/api/manufacturers/{manuf_id}'
        headers = {
            'Output-Format': 'JSON',
            'Authorization': f'{api_key}'
        }
        self.logger.info(
            '%s: Making GET request for manufacturer with id: %s' % (self.class_name, manuf_id))
        return self.get_meth(url, headers)

    @allure.step("Выполнение запроса создания поставщика")
    def create_supplier(self, api_key, supplier_name):
        url = "http://localhost:8082/api/suppliers"

        payload = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                   "<prestashop xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n"
                   "    <supplier>\n"
                   f"        <name>{supplier_name}</name>\n"
                   "    </supplier>\n"
                   "</prestashop>")
        headers = {
            'Output-Format': 'JSON',
            'Content-Type': 'application/xml',
            'Authorization': f'{api_key}'
        }
        self.logger.info(
            '%s: Making POST request for creating supplier with name: %s' % (self.class_name, supplier_name))
        resp = self.post_meth(url, headers, payload)
        return resp

    @allure.step("Выполнение запроса получения поставщика по id")
    def get_supplier_by_id(self, api_key, suppl_id):
        url = f'http://localhost:8082/api/suppliers/{suppl_id}'
        headers = {
            'Output-Format': 'JSON',
            'Authorization': f'{api_key}'
        }
        self.logger.info(
            '%s: Making GET request for supplier with id: %s' % (self.class_name, suppl_id))
        return self.get_meth(url, headers)

    @allure.step("Выполнение запроса создания категории")
    def create_category(self, api_key, category_name):
        url = "http://localhost:8082/api/categories"
        payload = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                   "<prestashop xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n"
                   "<category>\n"
                   "    <name>\n"
                   f"        <language id=\"1\"><![CDATA[{category_name}]]></language>\n"
                   "    </name>\n"
                   "    <link_rewrite>\n"
                   f"        <language id=\"1\"><![CDATA[{category_name}]]></language>\n"
                   "    </link_rewrite>\n"
                   "    <description>\n"
                   "        <language id=\"1\"><![CDATA[my awesome category description]]></language>\n"
                   "    </description>\n"
                   "    <active>1</active>\n"
                   "    <id_parent>1</id_parent>\n"
                   "</category>\n"
                   "</prestashop>")
        headers = {
            'Output-Format': 'JSON',
            'Content-Type': 'application/xml',
            'Authorization': f'{api_key}'
        }
        self.logger.info(
            '%s: Making POST request for creating category with name: %s' % (self.class_name, category_name))
        resp = self.post_meth(url, headers, payload)
        return resp

    @allure.step("Выполнение запроса получения категории по id")
    def get_category_by_id(self, api_key, cat_id):
        url = f'http://localhost:8082/api/suppliers/{cat_id}'
        headers = {
            'Output-Format': 'JSON',
            'Authorization': f'{api_key}'
        }
        self.logger.info(
            '%s: Making GET request for category with id: %s' % (self.class_name, cat_id))
        return self.get_meth(url, headers)

    @allure.step("Выполнение запроса создания товара")
    def create_product(
            self,
            api_key: str,
            name: str,
            id_manufacturer: int,
            id_supplier: int,
            id_category: int,
            id_brand=10,
            new=1,
            id_default_combination=1,
            id_tax_rules_group=1,
            type=1,
            reference=12345,
            supplier_reference='ABCDE',
            location='1234',
            width=11.1,
            height=22.2,
            depth=33.3,
            weight=44,
            quantity_discount=0,
            ean13=1,
            state=1,
            product_type='standard',
            price=123.4,
            unit_price=123.4,
            active=1,
            meta_description='some description',
            description='some description'
            ):

        url = "http://localhost:8082/api/products"
        payload = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                   "<prestashop xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n"
                   "<product>\n\t"
                   f"<id_manufacturer><![CDATA[{id_manufacturer}]]></id_manufacturer>\n\t"
                   f"<id_supplier><![CDATA[{id_supplier}]]></id_supplier>\n"
                   f"    <id_brand><![CDATA[{id_brand}]]></id_brand>\n\t"
                   f"<id_category_default><![CDATA[{id_category}]]></id_category_default>\n\t"
                   f"<new><![CDATA[{new}]]></new>\n\t"
                   f"<id_default_combination><![CDATA[{id_default_combination}]]></id_default_combination>\n\t"
                   f"<id_tax_rules_group><![CDATA[{id_tax_rules_group}]]></id_tax_rules_group>\n\t"
                   f"<type><![CDATA[1]]></type>\n\t"
                   f"<id_shop_default><![CDATA[{type}]]></id_shop_default>\n\t"
                   f"<reference><![CDATA[{reference}]]></reference>\n\t"
                   f"<supplier_reference><![CDATA[{supplier_reference}]]></supplier_reference>\n\t"
                   f"<location><![CDATA[{location}]]></location>\n\t"
                   f"<width><![CDATA[{width}]]></width>\n\t"
                   f"<height><![CDATA[{height}]]></height>\n\t"
                   f"<depth><![CDATA[{depth}]]></depth>\n\t"
                   f"<weight><![CDATA[{weight}]]></weight>\n\t"
                   f"<quantity_discount><![CDATA[{quantity_discount}]]></quantity_discount>\n\t"
                   f"<ean13><![CDATA[{ean13}]]></ean13>\n\t"
                   f"<state><![CDATA[{state}]]></state>\n\t"
                   f"<product_type><![CDATA[{product_type}]]></product_type>\n\t"
                   f"<price><![CDATA[{price}]]></price>\n\t"
                   f"<unit_price><![CDATA[{unit_price}]]></unit_price>\n\t"
                   f"<active><![CDATA[{active}]]></active>\n\t"
                   f"<meta_description><language id=\"1\"><![CDATA[{meta_description}]]></language><language id=\"2\">"
                   f"<![CDATA[{meta_description}]]></language></meta_description>\n\t"
                   f"<meta_keywords><language id=\"1\"><![CDATA[]]></language><language id=\"2\"><![CDATA[]]>"
                   "</language></meta_keywords>\n\t"
                   "<meta_title><language id=\"1\"><![CDATA[]]></language><language id=\"2\"><![CDATA[]]>"
                   "</language></meta_title>\n\t"
                   "<link_rewrite><language id=\"1\"><![CDATA[]]></language><language id=\"2\"><![CDATA[]]></language>"
                   "</link_rewrite>\n\t"
                   f"<name><language id=\"1\"><![CDATA[{name}]]></language><language id=\"2\"><![CDATA[{name}]]>"
                   "</language></name>\n\t"
                   f"<description><language id=\"1\"><![CDATA[{description}]]></language><language id=\"2\">"
                   f"<![CDATA[{description}]]></language></description>\n\t"
                   "<description_short><language id=\"1\"><![CDATA[]]></language><language id=\"2\"><![CDATA[]]>"
                   "</language></description_short>\n"
                   "    <associations>\n"
                   "        <categories>\n"
                   "            <category>\n"
                   f"                <id><![CDATA[{id_category}]]></id>\n"
                   "            </category>\n"
                   "        </categories>\n"
                   "    </associations>\n"
                   "</product>\n"
                   "</prestashop>")
        headers = {
            'Output-Format': 'JSON',
            'Content-Type': 'application/xml',
            'Authorization': f'{api_key}'
        }
        self.logger.info(
            '%s: Making POST request for creating pruduct with name: %s' % (self.class_name, name))
        resp = self.post_meth(url, headers, payload)
        return resp

    @allure.step("Выполнение запроса получения товарного запаса")
    def get_prod_stock(self, api_key, prod_id):
        url = f"http://localhost:8082/api/stock_availables?filter[id_product]={prod_id}&display=full&output_format=JSON"

        headers = {
            'Output-Format': 'JSON',
            'Authorization': f'{api_key}'
        }
        self.logger.info(
            '%s: Making GET request for product stock with id: %s' % (self.class_name, prod_id))
        resp = self.get_meth(url, headers)
        return resp


# print(update_product_stock('Basic MU5VVlFFS0VIM01NQU5IRlZaTDMxTUVaSEdJVEJKVDc6',21, 100).text)
# print(get_prod_stock('Basic MU5VVlFFS0VIM01NQU5IRlZaTDMxTUVaSEdJVEJKVDc6',21).text)
