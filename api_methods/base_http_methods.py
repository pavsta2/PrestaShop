import requests


def get_meth(url, params, headers):
    return requests.get(params=params, headers=headers, url=url)


def post_meth(url, params, headers, body):
    return requests.post(url=url, params=params, headers=headers, data=body)


def patch_meth(url, params, headers, body):
    return requests.patch(url=url, params=params, headers=headers, data=body)