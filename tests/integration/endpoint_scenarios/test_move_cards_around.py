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


def test_take_card_from_table(client, three_players):
    player_1 = three_players[0]
    player_2 = three_players[1]

    endpoint = "/api/table/{}/players/{}/table".format(
        player_1["table_name"], player_1["name"]
    )

    res = client.delete(endpoint, json=dict(signature=player_1["signature"], index=0))
    table_json = json.loads(res.data)
    assert res.status_code == 200
    assert len(table_json["cards"]) == 13 * 4 - 1

    res = client.delete(endpoint, json=dict(signature=player_2["signature"], index=0))
    res.status_code == 403


def test_give_card_to_table(client, three_players):
    player_1 = three_players[0]

    endpoint = "/api/table/{}/players/{}/table".format(
        player_1["table_name"], player_1["name"]
    )

    client.delete(endpoint, json=dict(signature=player_1["signature"], index=0))
    client.delete(endpoint, json=dict(signature=player_1["signature"], index=0))
    client.delete(endpoint, json=dict(signature=player_1["signature"], index=0))

    res = client.post(endpoint, json=dict(signature=player_1["signature"], index=0))

    table_json = json.loads(res.data)

    assert res.status_code == 200
    assert len(table_json["cards"]) == 13 * 4 - 3 + 1


def test_give_card_to_player(client, three_players_with_cards):
    for player in three_players_with_cards:
        assert len(player["cards"]) == 5

    player_1 = three_players_with_cards[0]
    player_2 = three_players_with_cards[1]

    endpoint = "/api/table/{}/players/{}/cards/{}".format(
        player_1["table_name"], player_1["name"], player_2["name"]
    )
    res = client.post(endpoint, json=dict(signature=player_1["signature"], index=0))

    assert res.status_code == 200

    endpoint = "/api/table/{}/players/{}".format(
        player_1["table_name"], player_1["name"]
    )
    res = client.get(endpoint)

    assert len(json.loads(res.data)["cards"]) == 4

    endpoint = "/api/table/{}/players/{}".format(
        player_2["table_name"], player_2["name"]
    )
    res = client.get(endpoint)

    assert len(json.loads(res.data)["cards"]) == 6


def test_take_card_from_player(client, three_players_with_cards):

    player_1 = three_players_with_cards[0]
    player_2 = three_players_with_cards[1]

    endpoint = "/api/table/{}/players/{}/cards/{}".format(
        player_1["table_name"], player_1["name"], player_2["name"]
    )
    res = client.delete(endpoint, json=dict(signature=player_1["signature"], index=0))

    assert res.status_code == 200

    endpoint = "/api/table/{}/players/{}".format(
        player_1["table_name"], player_1["name"]
    )
    res = client.get(endpoint)

    assert len(json.loads(res.data)["cards"]) == 6

    endpoint = "/api/table/{}/players/{}".format(
        player_2["table_name"], player_2["name"]
    )
    res = client.get(endpoint)

    assert len(json.loads(res.data)["cards"]) == 4
