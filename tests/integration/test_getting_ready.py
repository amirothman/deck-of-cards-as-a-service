from models.table import Table
from models.player import Player


def test_players_and_cards_on_a_table():
    # create players
    player_names = ["a", "b", "c"]
    players = [Player(name) for name in player_names]

    # players joining a table
    table = Table()
    second_table = Table()

    for player in players:
        player.join_table(table)

    assert table.players == players

    for player in players:
        assert player.table == table
        assert player.table != second_table
