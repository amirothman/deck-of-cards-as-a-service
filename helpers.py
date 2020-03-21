from constants import SUITS, NUMBERS
from models.card import Card


def get_deck_of_cards(**kwargs):
    deck = []
    for suit in SUITS:
        for number in NUMBERS:
            deck.append(Card(suit, number, **kwargs))
    return deck
