from uuid import uuid4
from .base import Base


class Player(Base):
    def __init__(self, name):
        self.cards = []
        self.name = name
        self.signature = str(uuid4())
        self.table_name = None

    def join_table(self, table):
        table.add_player(self)
        self.table_name = table.name

    def take_card_by_index(self, original_owner, index):
        """Take a card from someone/table by referencing
        its index

        Arguments:

            recepient (Player) - the person that will get the card
            index (int)
        """

        original_owner.give_card_by_index(self, index)
