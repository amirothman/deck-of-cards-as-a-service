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
def three_players_get_five_cards_each(players_and_table):
    players, table = players_and_table

    for player in players:
        for _ in range(5):
            table.give_card_by_index(player, 0)

    return players, table


def test_each_player_given_one_card(players_and_table):
    players, table = players_and_table

    cards_copy = table.cards.copy()
    for player in players:
        table.give_card_by_index(player, 0)

    for idx, player in enumerate(players):
        assert len(player.cards) == 1
        assert player.cards[0] == cards_copy[idx]
    assert len(table.cards) == 4 * 13 - 3


def test_each_player_given_five_cards(players_and_table):
    players, table = players_and_table

    for player in players:
        for _ in range(5):
            table.give_card_by_index(player, 0)

    for idx, player in enumerate(players):
        assert len(player.cards) == 5

    assert len(table.cards) == 4 * 13 - 5 * 3


def test_give_cards_to_a_player(three_players_get_five_cards_each):
    players, table = three_players_get_five_cards_each

    player_1 = players[0]
    player_2 = players[1]

    card_to_give = player_1.cards[0]
    player_1.give_card_by_index(player_2, 0)

    assert len(player_1.cards) == 4
    assert len(player_2.cards) == 6

    assert player_2.cards[-1] == card_to_give


def test_give_one_card_back_to_the_table(three_players_get_five_cards_each):
    players, table = three_players_get_five_cards_each

    player_1 = players[0]
    cards_to_give = player_1.cards[0]

    player_1.give_card_by_index(table, 0)

    assert len(table.cards) == 4 * 13 - 3 * 5 + 1
    assert table.cards[-1] == cards_to_give


def test_give_four_card_back_to_the_table(three_players_get_five_cards_each):
    players, table = three_players_get_five_cards_each

    player_1 = players[0]

    for _ in range(4):
        player_1.give_card_by_index(table, 0)

    assert len(table.cards) == 4 * 13 - 3 * 5 + 4


def test_take_cards_from_other_player(three_players_get_five_cards_each):
    players, table = three_players_get_five_cards_each

    player_1 = players[0]
    player_2 = players[1]

    player_1_cards = player_1.cards.copy()
    player_2_cards = player_2.cards.copy()

    player_1.take_card_by_index(player_2, 0)

    assert len(player_1.cards) == len(player_1_cards) + 1
    assert len(player_2.cards) == len(player_2_cards) - 1


def test_take_cards_from_table(three_players_get_five_cards_each):
    players, table = three_players_get_five_cards_each

    player_1 = players[0]

    original_cards_on_table = table.cards.copy()
    original_cards_player_1 = player_1.cards.copy()

    player_1.take_card_by_index(table, 0)
    assert len(player_1.cards) == len(original_cards_player_1) + 1
    assert len(table.cards) == len(original_cards_on_table) - 1
