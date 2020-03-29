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


@pytest.mark.skip
def test_read_revealed_cards_on_table(client, three_players_with_cards):
    player = three_players_with_cards[0]
    table_name = player["table_name"]

    endpoint = f"/api/table/{table_name}"
    res = client.get(endpoint)

    table = json.loads(res.data)
    endpoint = "/api/table/{}/card".format(player["table_name"])
    for idx, card in enumerate(table["cards"]):
        res = client.patch(endpoint, json=dict(index=idx, cover=False))

        assert res.status_code == 200

        endpoint = f"/api/table/{table_name}"
        res = client.get(endpoint)
        table = json.loads(res.data)
        import pdb

        pdb.set_trace()
        assert table["cards"][idx]["number"] != COVERED_LABEL
        assert table["cards"][idx]["suit"] != COVERED_LABEL
