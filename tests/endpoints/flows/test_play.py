import json

import pytest
import requests


from .helpers import build_url


@pytest.fixture
def default_table():
    endpoint = build_url("/table")
    res = requests.post(endpoint)
    return json.loads(res.content)


def test_create_table_endpoint():
    endpoint = build_url("/table")
    res = requests.post(endpoint)
    table = json.loads(res.content)
    name = table["name"]

    assert res.status_code == 200
    assert table["name"]
    assert table["cards"]
    assert table["players"] == []

    endpoint = build_url("/table/{}".format(name))
    res = requests.get(endpoint)
    assert res.status_code == 200
