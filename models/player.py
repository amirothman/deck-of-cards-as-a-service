from random import shuffle

from constants import TABLE
from models.table import Table


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.table = None

    def join_table(self, table: Table):
        table.add_player(self)
        self.table = table

    def shuffle_cards(self):
        shuffle(self.cards)

    def receive_card(self, card):
        """Add card to `self.cards`"""

        self.cards.append(card)

    def take_card_by_index(self, original_owner, index):
        """Take a card from someone/table by referencing
        its index

        Arguments:

            recepient (Player) - the person that will get the card
            index (int)
        """

        original_owner.give_card_by_index(self, index)

    def give_card_by_index(self, recepient, index):
        """Give a card away by referencing its index in
        the self.cards list.

        Arguments:

            recepient (Player) - the person that will get the card
            index (int)
        """

        try:
            self.cards[index].owner = recepient.name
        except AttributeError:
            if isinstance(recepient, Table):
                self.cards[index].owner = TABLE

        card = self.cards.pop(index)
        recepient.receive_card(card)
