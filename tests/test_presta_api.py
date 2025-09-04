import json
import random
import string
from datetime import datetime
from typing import Optional, List
import pytest
from pydantic import BaseModel
from api_methods.presta_api_methods import get_product_max_id
from api_methods.presta_api_methods import get_product
from api_methods.presta_api_methods import create_manufacture
from api_methods.presta_api_methods import get_manufacture_by_id
from api_methods.presta_api_methods import create_supplier
from api_methods.presta_api_methods import get_supplier_by_id
from api_methods.presta_api_methods import create_category
from api_methods.presta_api_methods import get_category_by_id
from api_methods.presta_api_methods import create_product


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
    unit_price_ratio: Optional[int] = None
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


def generate_random_string(length:int) -> str:
    return ''.join(random.choices(string.ascii_letters, k=length))


def test_get_prod_by_id_posit(get_api_key):
    api_key = get_api_key
    prod_id = get_product_max_id(api_key)
    resp = get_product(prod_id, api_key)
    assert resp.status_code == 200, f'Код ответа отличается от кода 200, text ответа: {resp.text}'

    assert resp.json()['product']['id'] == prod_id, f'Получен продукт с id:{resp.json()["product"]["id"]} вместо {prod_id} '


def test_get_prod_by_id_negot_no_such_id(get_api_key):
    api_key = get_api_key
    prod_id = get_product_max_id(api_key) + 1
    resp = get_product(prod_id, api_key)
    assert resp.status_code == 404, f'Код ответа отличается от кода 404, text ответа: {resp.text}'


@pytest.mark.parametrize('pr_id',
                         ['abcd',
                          '!@#$%^&*',
                          ' '
                          ],
                         ids=['letters',
                              'symbols',
                              'whitespace'
                              ])
def test_get_prod_by_id_negot_invalid_id(get_api_key, pr_id):
    api_key = get_api_key
    resp = get_product(pr_id, api_key)
    assert resp.status_code == 404, f'Код ответа отличается от кода 404, text ответа: {resp.text}'


@pytest.mark.parametrize('manuf_name',
                         [generate_random_string(65),
                          ''
                          ],
                         ids=['Name with invalid maxlenth > 64',
                              'Blanc string'
                              ])
def test_create_manufacturer_negot(get_api_key, manuf_name):
    api_key = get_api_key
    resp = create_manufacture(api_key, manuf_name)
    assert resp.status_code == 400, f'Возвратился код {resp.status_code} вместо 400, text: {resp.text}'


@pytest.mark.parametrize('manuf_name',
                         [generate_random_string(3),
                          generate_random_string(64)],
                         ids=['Valid manufacture name lenth 3',
                              'Valid manufacture name maxlenth 64'])
def test_create_manufacturer_posit(get_api_key, manuf_name):
    api_key = get_api_key
    resp = create_manufacture(api_key, manuf_name)
    assert resp.status_code == 201, f'Возвратился код {resp.status_code} вместо 201'

    assert resp.json()['manufacturer']['name'] == manuf_name, (f'Созданное имя {resp.json()["manufacturer"]["name"]} не'
                                                               f'соответствует заданному {manuf_name}')


@pytest.mark.parametrize('manuf_id',
                         [1],
                         ids=['First id'])
def test_get_manufacturer_by_id_posit(get_api_key, manuf_id):
    api_key = get_api_key
    resp = get_manufacture_by_id(api_key, manuf_id)
    assert resp.status_code == 200, f'Возвратился код {resp.status_code} вместо 200'


@pytest.mark.parametrize('manuf_id',
                         ['dfgt'],
                         ids=['Invalid ID format - string'])
def test_get_manufacturer_by_id_negot(get_api_key, manuf_id):
    api_key = get_api_key
    resp = get_manufacture_by_id(api_key, manuf_id)
    assert resp.status_code == 404, f'Возвратился код {resp.status_code} вместо 404'


@pytest.mark.parametrize('suppl_name',
                         [generate_random_string(65),
                          ''
                          ],
                         ids=['Name with invalid maxlenth > 64',
                              'Blanc string'
                              ])
def test_create_supplier_negot(get_api_key, suppl_name):
    api_key = get_api_key
    resp = create_supplier(api_key, suppl_name)
    assert resp.status_code == 400, f'Возвратился код {resp.status_code} вместо 400, text: {resp.text}'


@pytest.mark.parametrize('suppl_name',
                         [generate_random_string(3),
                          generate_random_string(64)],
                         ids=['Valid supplier name lenth 3',
                              'Valid supplier name maxlenth 64'])
def test_create_supplier_posit(get_api_key, suppl_name):
    api_key = get_api_key
    resp = create_supplier(api_key, suppl_name)
    assert resp.status_code == 201, f'Возвратился код {resp.status_code} вместо 201'

    assert resp.json()['supplier']['name'] == suppl_name, (f'Созданное имя {resp.json()["supplier"]["name"]} не'
                                                               f'соответствует заданному {suppl_name}')


@pytest.mark.parametrize('suppl_id',
                         [1],
                         ids=['First id'])
def test_get_supplier_by_id_posit(get_api_key, suppl_id):
    api_key = get_api_key
    resp = get_supplier_by_id(api_key, suppl_id)
    assert resp.status_code == 200, f'Возвратился код {resp.status_code} вместо 200'


@pytest.mark.parametrize('suppl_id',
                         ['dfgt'],
                         ids=['Invalid ID format - string'])
def test_get_supplier_by_id_negot(get_api_key, suppl_id):
    api_key = get_api_key
    resp = get_supplier_by_id(api_key, suppl_id)
    assert resp.status_code == 404, f'Возвратился код {resp.status_code} вместо 404'


@pytest.mark.parametrize('cat_name',
                         [generate_random_string(129),
                          ''
                          ],
                         ids=['Name with invalid maxlenth > 128',
                              'Blanc string'
                              ])
def test_create_category_negot(get_api_key, cat_name):
    api_key = get_api_key
    resp = create_category(api_key, cat_name)
    assert resp.status_code == 400, f'Возвратился код {resp.status_code} вместо 400, text: {resp.text}'


@pytest.mark.parametrize('cat_name',
                         [generate_random_string(3),
                          generate_random_string(128)],
                         ids=['Valid category name lenth 3',
                              'Valid category name maxlenth 128'])
def test_create_category_posit(get_api_key, cat_name):
    api_key = get_api_key
    resp = create_category(api_key, cat_name)
    assert resp.status_code == 201, f'Возвратился код {resp.status_code} вместо 201'

    assert resp.json()['category']['name'] == cat_name, (f'Созданное имя {resp.json()["category"]["name"]} не'
                                                               f'соответствует заданному {cat_name}')


@pytest.mark.parametrize('cat_name',
                         [1],
                         ids=['First id'])
def test_get_category_by_id_posit(get_api_key, cat_name):
    api_key = get_api_key
    resp = get_category_by_id(api_key, cat_name)
    assert resp.status_code == 200, f'Возвратился код {resp.status_code} вместо 200'


@pytest.mark.parametrize('cat_name',
                         ['dfgt'],
                         ids=['Invalid ID format - string'])
def test_get_category_by_id_negot(get_api_key, cat_name):
    api_key = get_api_key
    resp = get_category_by_id(api_key, cat_name)
    assert resp.status_code == 404, f'Возвратился код {resp.status_code} вместо 404'


@pytest.mark.parametrize('name, id_manufacturer, id_supplier, id_category, price',
                         [(generate_random_string(128), 1, 1, 1, 500),
                          ],
                         ids=['Valid values'])
def test_create_product_posit(get_api_key, name, id_manufacturer, id_supplier, id_category, price):
    api_key = get_api_key
    resp = create_product(api_key,
                          name=name,
                          id_manufacturer=id_manufacturer,
                          id_supplier=id_supplier,
                          id_category=id_category,
                          price=price)
    assert resp.status_code == 201, f'Возвратился код {resp.status_code} вместо 201, text ответа: {resp.text}'

    assert resp.json()['product']['name'] == name, (f'Созданное имя {resp.json()["product"]["name"]} не'
                                                               f'соответствует заданному {name}')


@pytest.mark.parametrize('name, id_manufacturer, id_supplier, id_category, price',
                         [(generate_random_string(129), 1, 1, 1, 500),
                          (generate_random_string(100), 1, 1, 1, 'abcd'),
                          (generate_random_string(100), 1, 1, 1, ' '),
                          (generate_random_string(100), 1, 1, 1, '')
                          ],
                         ids=['Name with invalid maxlenth > 128',
                              'Letters in price',
                              'Whitespace in price',
                              'No price'
                              ])
def test_create_product_negot(get_api_key, name, id_manufacturer, id_supplier, id_category, price):
    api_key = get_api_key
    resp = create_product(api_key,
                          name=name,
                          id_manufacturer=id_manufacturer,
                          id_supplier=id_supplier,
                          id_category=id_category,
                          price=price)
    assert resp.status_code == 400, f'Возвратился код {resp.status_code} вместо 400, text: {resp.text}'


