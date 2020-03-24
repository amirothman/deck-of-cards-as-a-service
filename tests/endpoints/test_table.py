import pytest

from app import create_app
from schemas import TableSchema


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
    table = TableSchema().load(res.json)
    assert table.name
    assert table.cards
    assert table.players == []


def test_get_table_endpoint(client):
    endpoint = "/table"
    res = client.post(endpoint)
    table = TableSchema().load(res.json)
    res = client.get("/table/{}".format(table.name))

    assert res.status_code == 200
