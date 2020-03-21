from helpers import get_deck_of_cards


def test_deck_of_cards_default():
    cards = get_deck_of_cards()
    assert cards
    assert len(cards) == 4 * 13


def test_deck_of_cards_to_player():
    cards = get_deck_of_cards(owner="amir")
    for card in cards:
        assert card.owner == "amir"


def test_deck_of_cards_to_player_uncovered():
    cards = get_deck_of_cards(owner="amir", covered=False)
    for card in cards:
        assert card.owner == "amir"
        assert not card.covered
