from random import shuffle

from helpers import get_deck_of_cards


class Table:
    def __init__(self):
        self.cards = get_deck_of_cards()
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def shuffle_cards(self):
        shuffle(self.cards)

    def receive_card(self, card):
        """Add card to `self.cards`"""

        self.cards.append(card)

    def give_card_by_index(self, recepient, index):
        """Give a card away by referencing its index in
        the self.cards list.

        Arguments:

            recepient (Player) - the person that will get the card
            index (int)
        """

        self.cards[index].owner = recepient.name
        card = self.cards.pop(index)
        recepient.receive_card(card)
