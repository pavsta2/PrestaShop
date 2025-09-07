from datetime import datetime
from typing import Optional, List
import allure
import pytest
from pydantic import BaseModel
from api_methods.presta_api_methods import ApiRequest
from pages.base_page import BasePage


class CategoryAssociation(BaseModel):
    id: Optional[int] = None


class StockAvailableAssociation(BaseModel):
    id: Optional[int] = None
    id_product_attribute: Optional[int] = None


class Associations(BaseModel):
    categories: List[CategoryAssociation]
    stock_availables: List[StockAvailableAssociation]


class Product(BaseModel):
    id: int
    id_manufacturer: Optional[int] = None
    id_supplier: Optional[int] = None
    id_category_default: Optional[int] = None
    new: Optional[int] = None
    cache_default_attribute: Optional[int] = None
    id_tax_rules_group: Optional[int] = None
    position_in_category: Optional[int] = None
    manufacturer_name: Optional[str] = None
    type: Optional[str] = None
    id_shop_default: Optional[int] = None
    reference: Optional[str] = None
    supplier_reference: Optional[str] = None
    location: Optional[str] = None
    width: Optional[float] = None
    height: Optional[float] = None
    depth: Optional[float] = None
    weight: Optional[float] = None
    quantity_discount: Optional[bool] = 0
    ean13: Optional[str] = None
    mpn: Optional[str] = None
    state: Optional[int] = None
    product_type: Optional[str] = None
    price: float
    wholesale_price: Optional[float] = None
    unit_price: Optional[float] = None
    unit_price_ratio: Optional[float] = None
    active: Optional[int] = None
    available_for_order: Optional[int] = None
    condition: Optional[str] = None
    visibility: Optional[str] = None
    date_add: Optional[datetime] = None
    date_upd: Optional[datetime] = None
    meta_description: Optional[str] = None
    link_rewrite: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    associations: Associations


@allure.feature('Проверки Presta Api')
class TestApi:
    """Проверки API"""

    @allure.title("Позитивная проверка получения товара по id")
    def test_get_prod_by_id_posit(self, get_api_key, logger):
        api_key = get_api_key
        prod_id = ApiRequest(logger).get_product_max_id(api_key)
        resp = ApiRequest(logger).get_product(api_key, prod_id)
        assert resp.status_code == 200, f'Код ответа отличается от кода 200, text ответа: {resp.text}'

        assert resp.json()['product']['id'] == prod_id, f'Получен продукт с id:{resp.json()["product"]["id"]} вместо {prod_id} '

    @allure.title("Проверка полученного json, описывающего один товар")
    def test_prod_json(self, get_api_key, logger):
        api_key = get_api_key
        prod_id = ApiRequest(logger).get_product_max_id(api_key)
        resp = ApiRequest(logger).get_product(api_key, prod_id)

        Product.model_validate(resp.json()['product'])

    @allure.title("Негативная проверка получения товара по несуществующему id")
    def test_get_prod_by_id_negot_no_such_id(self, get_api_key, logger):
        api_key = get_api_key
        prod_id = ApiRequest(logger).get_product_max_id(api_key) + 1
        resp = ApiRequest(logger).get_product(api_key, prod_id)
        assert resp.status_code == 404, f'Код ответа отличается от кода 404, text ответа: {resp.text}'

    @allure.title("Негативная проверка получения товара по невалидному id")
    @pytest.mark.parametrize('pr_id',
                             ['abcd',
                              '!@#$%^&*',
                              ' '
                              ],
                             ids=['letters',
                                  'symbols',
                                  'whitespace'
                                  ])
    def test_get_prod_by_id_negot_invalid_id(self, get_api_key, logger, pr_id):
        api_key = get_api_key
        resp = ApiRequest(logger).get_product(api_key, pr_id)
        assert resp.status_code == 404, f'Код ответа отличается от кода 404, text ответа: {resp.text}'

    @allure.title("Негативная проверка создания производителя с невалидным именем")
    @pytest.mark.parametrize('manuf_name',
                             [BasePage.generate_random_string(65),
                              ''
                              ],
                             ids=['Name with invalid maxlenth > 64',
                                  'Blanc string'
                                  ])
    def test_create_manufacturer_negot(self, get_api_key, manuf_name, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).create_manufacture(api_key, manuf_name)
        assert resp.status_code == 400, f'Возвратился код {resp.status_code} вместо 400, text: {resp.text}'

    @allure.title("Позитивная проверка создания производителя")
    @pytest.mark.parametrize('manuf_name',
                             [BasePage.generate_random_string(3),
                              BasePage.generate_random_string(64)],
                             ids=['Valid manufacture name lenth 3',
                                  'Valid manufacture name maxlenth 64'])
    def test_create_manufacturer_posit(self, get_api_key, manuf_name, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).create_manufacture(api_key, manuf_name)
        assert resp.status_code == 201, f'Возвратился код {resp.status_code} вместо 201'

        assert resp.json()['manufacturer']['name'] == manuf_name, (f'Созданное имя {resp.json()["manufacturer"]["name"]} не'
                                                                   f'соответствует заданному {manuf_name}')

    @allure.title("Позитивная проверка получения производителя по id")
    @pytest.mark.parametrize('manuf_id',
                             [1],
                             ids=['First id'])
    def test_get_manufacturer_by_id_posit(self, get_api_key, manuf_id, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).get_manufacture_by_id(api_key, manuf_id)
        assert resp.status_code == 200, f'Возвратился код {resp.status_code} вместо 200'

    @allure.title("Неготивная проверка получения производителя по невалидному id")
    @pytest.mark.parametrize('manuf_id',
                             ['dfgt'],
                             ids=['Invalid ID format - string'])
    def test_get_manufacturer_by_id_negot(self, get_api_key, manuf_id, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).get_manufacture_by_id(api_key, manuf_id)
        assert resp.status_code == 404, f'Возвратился код {resp.status_code} вместо 404'

    @allure.title("Неготивная проверка создания поставщика с невалидным именем")
    @pytest.mark.parametrize('suppl_name',
                             [BasePage.generate_random_string(65),
                              ''
                              ],
                             ids=['Name with invalid maxlenth > 64',
                                  'Blanc string'
                                  ])
    def test_create_supplier_negot(self, get_api_key, suppl_name, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).create_supplier(api_key, suppl_name)
        assert resp.status_code == 400, f'Возвратился код {resp.status_code} вместо 400, text: {resp.text}'

    @allure.title("Позитивная проверка создания поставщика")
    @pytest.mark.parametrize('suppl_name',
                             [BasePage.generate_random_string(3),
                              BasePage.generate_random_string(64)],
                             ids=['Valid supplier name lenth 3',
                                  'Valid supplier name maxlenth 64'])
    def test_create_supplier_posit(self, get_api_key, suppl_name, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).create_supplier(api_key, suppl_name)
        assert resp.status_code == 201, f'Возвратился код {resp.status_code} вместо 201'

        assert resp.json()['supplier']['name'] == suppl_name, (f'Созданное имя {resp.json()["supplier"]["name"]} не'
                                                                   f'соответствует заданному {suppl_name}')

    @allure.title("Позитивная проверка получения поставщика по id")
    @pytest.mark.parametrize('suppl_id',
                             [1],
                             ids=['First id'])
    def test_get_supplier_by_id_posit(self, get_api_key, suppl_id, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).get_supplier_by_id(api_key, suppl_id)
        assert resp.status_code == 200, f'Возвратился код {resp.status_code} вместо 200'

    @allure.title("Неготивная проверка получения поставщика оп невалидному id")
    @pytest.mark.parametrize('suppl_id',
                             ['dfgt'],
                             ids=['Invalid ID format - string'])
    def test_get_supplier_by_id_negot(self, get_api_key, suppl_id, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).get_supplier_by_id(api_key, suppl_id)
        assert resp.status_code == 404, f'Возвратился код {resp.status_code} вместо 404'

    @allure.title("Неготивная проверка создания категории с невалидным именем")
    @pytest.mark.parametrize('cat_name',
                             [BasePage.generate_random_string(129),
                              ''
                              ],
                             ids=['Name with invalid maxlenth > 128',
                                  'Blanc string'
                                  ])
    def test_create_category_negot(self, get_api_key, cat_name, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).create_category(api_key, cat_name)
        assert resp.status_code == 400, f'Возвратился код {resp.status_code} вместо 400, text: {resp.text}'

    @allure.title("Позитивная проверка создания категории")
    @pytest.mark.parametrize('cat_name',
                             [BasePage.generate_random_string(3),
                              BasePage.generate_random_string(128)],
                             ids=['Valid category name lenth 3',
                                  'Valid category name maxlenth 128'])
    def test_create_category_posit(self, get_api_key, cat_name, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).create_category(api_key, cat_name)
        assert resp.status_code == 201, f'Возвратился код {resp.status_code} вместо 201'

        assert resp.json()['category']['name'] == cat_name, (f'Созданное имя {resp.json()["category"]["name"]} не'
                                                                   f'соответствует заданному {cat_name}')

    @allure.title("Позитивная проверка получения категории")
    @pytest.mark.parametrize('cat_name',
                             [1],
                             ids=['First id'])
    def test_get_category_by_id_posit(self, get_api_key, cat_name, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).get_category_by_id(api_key, cat_name)
        assert resp.status_code == 200, f'Возвратился код {resp.status_code} вместо 200'

    @allure.title("Неготивная проверка получения категории по невалидному id")
    @pytest.mark.parametrize('cat_name',
                             ['dfgt'],
                             ids=['Invalid ID format - string'])
    def test_get_category_by_id_negot(self, get_api_key, cat_name, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).get_category_by_id(api_key, cat_name)
        assert resp.status_code == 404, f'Возвратился код {resp.status_code} вместо 404'

    @allure.title("Позитивная проверка создания товара")
    @pytest.mark.parametrize('name, id_manufacturer, id_supplier, id_category, price',
                             [(BasePage.generate_random_string(128), 1, 1, 1, 500),
                              ],
                             ids=['Valid values'])
    def test_create_product_posit(self, get_api_key, name, id_manufacturer, id_supplier, id_category, price, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).create_product(api_key,
                              name=name,
                              id_manufacturer=id_manufacturer,
                              id_supplier=id_supplier,
                              id_category=id_category,
                              price=price)
        assert resp.status_code == 201, f'Возвратился код {resp.status_code} вместо 201, text ответа: {resp.text}'

        assert resp.json()['product']['name'] == name, (f'Созданное имя {resp.json()["product"]["name"]} не'
                                                                   f'соответствует заданному {name}')

    @allure.title("Неготивная проверка создания товара с невалидными параметрами")
    @pytest.mark.parametrize('name, id_manufacturer, id_supplier, id_category, price',
                             [(BasePage.generate_random_string(129), 1, 1, 1, 500),
                              (BasePage.generate_random_string(100), 1, 1, 1, 'abcd'),
                              (BasePage.generate_random_string(100), 1, 1, 1, ' '),
                              (BasePage.generate_random_string(100), 1, 1, 1, '')
                              ],
                             ids=['Name with invalid maxlenth > 128',
                                  'Letters in price',
                                  'Whitespace in price',
                                  'No price'
                                  ])
    def test_create_product_negot(self, get_api_key, name, id_manufacturer, id_supplier, id_category, price, logger):
        api_key = get_api_key
        resp = ApiRequest(logger).create_product(api_key,
                              name=name,
                              id_manufacturer=id_manufacturer,
                              id_supplier=id_supplier,
                              id_category=id_category,
                              price=price)
        assert resp.status_code == 400, f'Возвратился код {resp.status_code} вместо 400, text: {resp.text}'
