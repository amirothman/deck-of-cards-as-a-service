import pytest

from models.table import Table
from models.player import Player


@pytest.fixture
def players_and_table():
    # create players
    player_names = ["a", "b", "c"]
    players = [Player(name) for name in player_names]

    # players joining a table
    table = Table()

    for player in players:
        player.join_table(table)

    return players, table


@pytest.fixture
def three_players_with_two_cards_each(players_and_table):
    players, table = players_and_table

    for player in players:
        for _ in range(2):
            table.give_card_by_index(player, 0)

    return players, table
