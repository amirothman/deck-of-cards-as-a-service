import json

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_create_table_endpoint(client):
    endpoint = "/table"
    res = client.post(endpoint)
    assert res.status_code == 200
    table = json.loads(res.data)

    assert table["name"]
    assert table["cards"]
    assert table["players"] == []
