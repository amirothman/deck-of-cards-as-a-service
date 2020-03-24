from models.card import get_deck_of_cards
from models.table import Table


def test_table():
    table = Table()
    deck_of_cards = get_deck_of_cards()
    label_deck_of_cards = [(c.suit, c.number) for c in deck_of_cards]
    label_deck_of_cards_on_table = [(c.suit, c.number) for c in table.cards]

    assert label_deck_of_cards == label_deck_of_cards_on_table
