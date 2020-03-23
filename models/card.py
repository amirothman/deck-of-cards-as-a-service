from constants import TABLE


def _has_read_permission(owner, reader, covered):
    return (owner == TABLE and not covered) or (owner == reader.name) or (not covered)


def _has_flip_permission(owner, flipper):
    return (owner == TABLE) or (owner == flipper.name)


class Card:
    def __init__(self, suit, number, covered=True, owner=TABLE):
        self.suit = suit
        self.number = number
        self.covered = covered
        self.owner = owner

    def read(self, reader):
        """Read the card

        Arguments:

            reader (Player) - The player who is reading the card

        Returns:

            (str, str) - Tuple of (suit, number)
        """
        if _has_read_permission(self.owner, reader, self.covered):
            return self.suit, self.number
        else:
            raise AttributeError(
                "Reader does not have permission. card.owner: {}, "
                "card.covered: {}, reader.name: {}".format(
                    self.owner, self.covered, reader.name
                )
            )

    def reveal(self, revealer):
        if _has_flip_permission(self.owner, revealer):
            self.covered = False
        else:
            raise AttributeError(
                "Reader does not have permission. card.owner: {}, "
                "revealer.name: {}".format(self.owner, revealer.name)
            )

    def cover(self, coverer):
        if _has_flip_permission(self.owner, coverer):
            self.covered = True
        else:
            raise AttributeError(
                "Reader does not have permission. card.owner: {}, "
                "coverer.name: {}".format(self.owner, coverer.name)
            )
