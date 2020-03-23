from random import shuffle


class Base:
    def shuffle_cards(self):
        shuffle(self.cards)

    def receive_card(self, card):
        """Add card to `self.cards`"""

        self.cards.append(card)

    def give_card_by_index(self, recepient, index):
        """Give a card away by referencing its index in
        the self.cards list.

        Arguments:

            recepient (Player|Table) - the person that will get the card
            index (int)
        """

        try:
            self.cards[index].owner = recepient.name
        except AttributeError:
            # have to import as such to avoid
            # cyclical imports :/
            from constants import TABLE
            from models.table import Table

            if isinstance(recepient, Table):
                self.cards[index].owner = TABLE

        card = self.cards.pop(index)
        recepient.receive_card(card)
