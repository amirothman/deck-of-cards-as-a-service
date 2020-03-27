import json

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def table_json(client):
    endpoint = "/api/table"
    res = client.post(endpoint)
    return json.loads(res.data)


@pytest.fixture
def three_players(client, table_json):

    endpoint = "/api/table/{}/players".format(table_json["name"])
    players = []
    for idx in range(3):
        res = client.post(endpoint, json=dict(name="player_{}".format(idx)))
        json_player = json.loads(res.data)
        players.append(json_player)

    return players


@pytest.fixture
def three_players_with_cards(client, three_players):
    three_players = three_players.copy()
    for player in three_players:
        endpoint = "/api/table/{}/players/{}/table".format(
            player["table_name"], player["name"]
        )
        for _ in range(5):
            client.delete(endpoint, json=dict(signature=player["signature"], index=0))
    three_players_ = []
    for player in three_players:
        res = client.get(
            "/api/table/{}/players/{}".format(player["table_name"], player["name"])
        )
        three_players_.append(json.loads(res.data))

    return three_players_
