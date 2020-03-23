from helpers import get_deck_of_cards
from .base import Base


class Table(Base):
    def __init__(self):
        self.cards = get_deck_of_cards()
        self.players = []

    def add_player(self, player):
        self.players.append(player)
