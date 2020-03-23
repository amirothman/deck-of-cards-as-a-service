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


def test_reading_own_cards(three_players_with_two_cards_each):
    players, table = three_players_with_two_cards_each
    player = players[0]

    for card in player.cards:
        assert card.read(player)


def test_player_cannot_reading_covered_cards_on_table(
    three_players_with_two_cards_each,
):
    players, table = three_players_with_two_cards_each

    for player in players:
        for card in table.cards:
            with pytest.raises(AttributeError):
                assert card.read(player)


def test_reading_uncovered_cards_on_table(three_players_with_two_cards_each):
    players, table = three_players_with_two_cards_each

    for player in players:
        for card in table.cards:
            if card.covered:
                card.reveal(player)
            assert card.read(player)


def test_players_cannot_read_covered_cards_on_table(three_players_with_two_cards_each):
    players, table = three_players_with_two_cards_each

    for player in players:
        for card in table.cards:
            with pytest.raises(AttributeError):
                card.read(player)


def test_players_cannot_read_covered_cards_from_other_player(
    three_players_with_two_cards_each,
):
    players, table = three_players_with_two_cards_each

    for player in players:
        for other_player in players:
            if player == other_player:
                continue
            else:
                for card in other_player.cards:
                    with pytest.raises(AttributeError):
                        card.read(player)


def test_players_can_read_uncovered_cards_from_other_player(
    three_players_with_two_cards_each,
):
    players, table = three_players_with_two_cards_each

    # uncovering cards
    for player in players:
        for card in player.cards:
            card.reveal(player)

    for player in players:
        for other_player in players:
            if player == other_player:
                continue
            else:
                for card in other_player.cards:
                    assert card.read(player)


def test_players_cannot_reveal_others_cards(three_players_with_two_cards_each):
    players, table = three_players_with_two_cards_each
    for player in players:
        for other_player in players:
            if player == other_player:
                continue
            else:
                for card in other_player.cards:
                    with pytest.raises(AttributeError):
                        assert card.reveal(player)
