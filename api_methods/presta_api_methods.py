
from .base_http_methods import get_meth, post_meth, patch_meth


def get_product(prod_id:int, api_key):
    url = f'http://localhost:8080/api/products/{prod_id}'
    headers = {
        'Output-Format': 'JSON',
        'Authorization': f'{api_key}',
        'Content-Type': 'text/plain'
    }
    return get_meth(url,'',headers)


def get_products(api_key):
    url = f'http://localhost:8080/api/products'
    headers = {
        'Output-Format': 'JSON',
        'Authorization': f'{api_key}',
    }
    return get_meth(url,'',headers)


def get_product_max_id(api_key):
    url = f'http://localhost:8080/api/products'
    headers = {
        'Output-Format': 'JSON',
        'Authorization': f'{api_key}',
    }
    return get_meth(url,'',headers).json()['products'][-1]['id']


def create_manufacture(api_key, manufacture_name):
    url = "http://localhost:8080/api/manufacturers"

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

    resp = post_meth(url,'', headers, payload)

    return resp


def get_manufacture_by_id(api_key, manuf_id):
    url = f'http://localhost:8080/api/manufacturers/{manuf_id}'
    headers = {
        'Output-Format': 'JSON',
        'Authorization': f'{api_key}'
    }
    return get_meth(url, '', headers)


def create_supplier(api_key, supplier_name):
    url = "http://localhost:8080/api/suppliers"

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

    resp = post_meth(url,'', headers, payload)
    return resp


def get_supplier_by_id(api_key, suppl_id):
    url = f'http://localhost:8080/api/suppliers/{suppl_id}'
    headers = {
        'Output-Format': 'JSON',
        'Authorization': f'{api_key}'
    }
    return get_meth(url, '', headers)


def create_category(api_key, category_name):
    url = "http://localhost:8080/api/categories"
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

    resp = post_meth(url, '', headers, payload)
    return resp


def get_category_by_id(api_key, cat_id):
    url = f'http://localhost:8080/api/suppliers/{cat_id}'
    headers = {
        'Output-Format': 'JSON',
        'Authorization': f'{api_key}'
    }
    return get_meth(url, '', headers)


def create_product(
        api_key:str,
        name:int,
        id_manufacturer:int,
        id_supplier:int,
        id_category:int,
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

    url = "http://localhost:8080/api/products"
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

    resp = post_meth(url, '', headers, payload)
    return resp


def get_prod_stock(api_key, prod_id):
    url = f"http://localhost:8080/api/stock_availables?filter[id_product]={prod_id}&display=full&output_format=JSON"

    headers = {
        'Output-Format': 'JSON',
        'Authorization': f'{api_key}'
    }

    resp = get_meth(url, '', headers)
    return resp


def update_product_stock(api_key, prod_id, quantity):
    stock_id = get_prod_stock(api_key, prod_id).json()['stock_availables'][0]['id']
    url = "http://localhost:8080/api/stock_availables/{{id_stock_available}}"

    payload = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
               "<prestashop xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n"
               "    <stock_available>\n"
               f"        <id><![CDATA[{stock_id}]]></id>\n"
               f"        <quantity><![CDATA[{quantity}]]></quantity>\n"
               "    </stock_available>\n"
               "</prestashop>")
    headers = {
        'Content-Type': 'application/xml',
        'Authorization': f'{api_key}'
    }

    resp = patch_meth(url, '', headers, payload)
    return resp


def update_prod_name(api_key, prod_id, new_prod_name):
    url = "http://localhost:8080/api/products/1"

    payload = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
               "<prestashop xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n"
               "    <product>\n"
               f"        <id><![CDATA[{prod_id}]]></id>\n\t"
               "    <name>\n"
               f"            <language id=\"1\"><![CDATA[{new_prod_name}]]></language>\n"
               f"            <language id=\"2\"><![CDATA[{new_prod_name}]]></language>\n"
               "        </name>\n"
               "    </product>\n"
               "</prestashop>")
    headers = {
        'Output-Format': 'JSON',
        'Content-Type': 'text/plain',
        'Authorization': f'{api_key}'
    }
    resp = patch_meth(url, '', headers, payload)
    return resp

# print(update_product_stock('Basic MU5VVlFFS0VIM01NQU5IRlZaTDMxTUVaSEdJVEJKVDc6',21, 100).text)
# print(get_prod_stock('Basic MU5VVlFFS0VIM01NQU5IRlZaTDMxTUVaSEdJVEJKVDc6',21).text)
