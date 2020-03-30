import json

import pytest

from constants import COVERED_LABEL


def test_read_covered_cards_on_table(client, three_players_with_cards):
    player = three_players_with_cards[0]
    table_name = player["table_name"]

    endpoint = f"/api/table/{table_name}"
    res = client.get(endpoint)

    table = json.loads(res.data)
    for card in table["cards"]:
        assert card["suit"] == COVERED_LABEL
        assert card["number"] == COVERED_LABEL


def test_read_revealed_cards_on_table(client, three_players_with_cards):
    player = three_players_with_cards[0]
    table_name = player["table_name"]

    endpoint = f"/api/table/{table_name}"
    res = client.get(endpoint)

    table = json.loads(res.data)
    endpoint = "/api/table/{}/card".format(player["table_name"])
    for idx, card in enumerate(table["cards"]):
        res_patch = client.patch(endpoint, json=dict(index=idx, cover=False))
        assert res_patch.status_code == 200

        table_endpoint = f"/api/table/{table_name}"
        res = client.get(table_endpoint)

        table = json.loads(res.data)
        assert table["cards"][idx]["number"] != COVERED_LABEL
        assert table["cards"][idx]["suit"] != COVERED_LABEL
