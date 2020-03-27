import json


def test_create_table_endpoint(client):
    endpoint = "/api/table"
    res = client.post(endpoint)
    assert res.status_code == 200
    table = json.loads(res.data)
    assert table["name"]
    assert table["cards"]
    assert table["players"] == []

    res = client.get("/api/table/{}".format(table["name"]))

    assert res.status_code == 200


def test_create_a_new_player_on_a_table(client, table_json):
    table_name = table_json["name"]
    endpoint = "/api/table/{}/players".format(table_name)

    # can create a new player on a table
    res = client.post(endpoint, json=dict(name="amir"))
    player = json.loads(res.data)

    assert res.status_code == 200
    assert player["table_name"] == table_name

    # check that the new player is indeed on the table
    res = client.get("/api/table/{}".format(table_name))
    table = json.loads(res.data)

    assert player in table["players"]
    player_name = player["name"]

    # check that the new player info can be retrieved
    player_res = client.get("/api/table/{}/players/{}".format(table_name, player_name))
    player = json.loads(player_res.data)

    assert player_name == player["name"]
    assert table_name == player["table_name"]
