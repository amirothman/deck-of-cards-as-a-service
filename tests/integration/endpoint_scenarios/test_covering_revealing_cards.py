import json

import pytest


@pytest.fixture
def player_with_an_uncovered_card(client, three_players_with_cards):
    player = three_players_with_cards[0]
    endpoint = "/api/table/{}/player/{}/card".format(
        player["table_name"], player["name"]
    )
    client.patch(
        endpoint, json=dict(signature=player["signature"], index=0, cover=False)
    )

    endpoint = "/api/table/{}/players/{}".format(player["table_name"], player["name"])
    res = client.get(endpoint)

    return json.loads(res.data)


@pytest.fixture
def one_player_with_an_uncovered_card(client, three_players_with_cards):
    player = three_players_with_cards[0]
    endpoint = "/api/table/{}/player/{}/card".format(
        player["table_name"], player["name"]
    )
    client.patch(
        endpoint, json=dict(signature=player["signature"], index=0, cover=False)
    )

    endpoint = "/api/table/{}/players/{}".format(player["table_name"], player["name"])
    res = client.get(endpoint)

    return [json.loads(res.data)] + three_players_with_cards[1:]


def test_can_reveal_own_card(client, three_players_with_cards):
    player = three_players_with_cards[0]
    endpoint = "/api/table/{}/player/{}/card".format(
        player["table_name"], player["name"]
    )
    client.patch(
        endpoint, json=dict(signature=player["signature"], index=0, cover=False)
    )

    endpoint = "/api/table/{}/player/{}/card/{}/{}".format(
        player["table_name"], player["name"], 0, player["signature"]
    )
    res = client.get(endpoint)
    card_json = json.loads(res.data)

    assert card_json["covered"] is False


def test_can_cover_own_card(client, player_with_an_uncovered_card):
    player = player_with_an_uncovered_card
    endpoint = "/api/table/{}/player/{}/card".format(
        player["table_name"], player["name"],
    )
    client.patch(
        endpoint, json=dict(signature=player["signature"], index=0, cover=True)
    )
    endpoint = "/api/table/{}/player/{}/card/{}/{}".format(
        player["table_name"], player["name"], 0, player["signature"]
    )
    res = client.get(endpoint)
    card_json = json.loads(res.data)

    assert card_json["covered"] is True


def test_cannot_cover_card_of_other_players(client, one_player_with_an_uncovered_card):
    player_1 = one_player_with_an_uncovered_card[0]

    player_2 = one_player_with_an_uncovered_card[1]

    endpoint = "/api/table/{}/player/{}/card".format(
        player_1["table_name"], player_1["name"],
    )
    res = client.patch(
        endpoint, json=dict(signature=player_2["signature"], index=0, cover=True)
    )
    assert res.status_code == 405


def test_cannot_reveal_card_of_other_players(client, three_players_with_cards):
    player_1 = three_players_with_cards[0]

    player_2 = three_players_with_cards[1]

    endpoint = "/api/table/{}/player/{}/card".format(
        player_1["table_name"], player_1["name"],
    )
    res = client.patch(
        endpoint, json=dict(signature=player_2["signature"], index=0, cover=False)
    )
    assert res.status_code == 405


def test_can_reveal_card_from_table(client, three_players_with_cards):
    player = three_players_with_cards[0]
    table_name = player["table_name"]
    endpoint = "/api/table/{}/card".format(player["table_name"])
    res = client.patch(endpoint, json=dict(index=0, cover=True))

    assert res.status_code == 200

    table_endpoint = "/api/table/{}".format(table_name)
    res = client.get(table_endpoint)
    table_json = json.loads(res.data)
    assert table_json["cards"][0]["covered"] is True


def test_can_cover_card_from_table(client, three_players_with_cards):
    player = three_players_with_cards[0]
    table_name = player["table_name"]
    endpoint = "/api/table/{}/card".format(player["table_name"])
    res = client.patch(endpoint, json=dict(index=0, cover=True))

    assert res.status_code == 200

    client.patch(endpoint, json=dict(index=0, cover=False))
    table_endpoint = "/api/table/{}".format(table_name)
    res = client.get(table_endpoint)
    table_json = json.loads(res.data)

    assert table_json["cards"][0]["covered"] is False
