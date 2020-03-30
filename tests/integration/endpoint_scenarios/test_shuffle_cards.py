def test_shuffle_cards_on_table(client, table_json):
    table_name = table_json["name"]
    endpoint = f"/api/table/{table_name}/cards"
    res = client.patch(endpoint)
    assert res.status_code == 200


def test_shuffle_cards_on_player(client, three_players_with_cards):
    player = three_players_with_cards[0]
    table_name = player["table_name"]
    player_name = player["name"]

    endpoint = f"/api/table/{table_name}/player/{player_name}/cards"
    res = client.patch(endpoint, json=dict(signature=player["signature"]))

    assert res.status_code == 200


def test_cannot_shuffle_cards_from_other_player(client, three_players_with_cards):
    player = three_players_with_cards[0]
    table_name = player["table_name"]
    player_name = player["name"]

    player_2 = three_players_with_cards[1]

    endpoint = f"/api/table/{table_name}/player/{player_name}/cards"
    res = client.patch(endpoint, json=dict(signature=player_2["signature"]))

    assert res.status_code == 405
