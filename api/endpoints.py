from collections import defaultdict

from flask import jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import Forbidden

from models.table import Table

from schemas import (
    CardActionSchema,
    CardSchema,
    CoverCardSchema,
    HidableCardSchema,
    PlayerSchema,
    TableSchema,
)

tables = {}
players = defaultdict(dict)


class TableAPI(MethodView):
    def get(self, table_name):
        """Get in info about the table"""
        # get table
        table = tables[table_name]

        dump = TableSchema().dump(table)
        return jsonify(dump)

    def post(self):
        """Create a new table"""
        # create a new table
        table = Table()
        tables[table.name] = table

        dump = TableSchema().dump(table)
        return jsonify(dump)


class PlayerAPI(MethodView):
    schema = PlayerSchema()

    def get(self, table_name, player_name):
        """Get info about a player"""
        if player_name:
            return jsonify(self.schema.dump(players[table_name][player_name]))

        return jsonify(self.schema.dump(players[table_name].values(), many=True))

    def post(self, table_name):
        """Create a new player on the table"""
        player = self.schema.load(request.get_json())

        # join the table
        player.join_table(tables[table_name])

        # persist to memory
        players[table_name][player.name] = player

        return jsonify(self.schema.dump(player))


class PlayersCardsAPI(MethodView):
    card_action_schema = CardActionSchema()
    player_schema = PlayerSchema()

    def post(self, table_name, current_name, other_name):
        """Give card from current_name to other_name"""

        current_player = players[table_name][current_name]
        give_card = self.card_action_schema.load(request.get_json())

        if give_card["signature"] == current_player.signature:
            recepient = players[table_name][other_name]
            current_player.give_card_by_index(recepient, give_card["index"])
            return jsonify(self.player_schema.dump(recepient))
        else:
            return (
                Forbidden(
                    description="Not allowed",
                    response=jsonify(dict(msg="Not allowed.")),
                ),
                405,
            )

    def delete(self, table_name, current_name, other_name):
        """Take card from other_name to current_name"""

        current_player = players[table_name][current_name]
        take_card = self.card_action_schema.load(request.get_json())

        if take_card["signature"] == current_player.signature:
            original_owner = players[table_name][other_name]
            current_player.take_card_by_index(original_owner, take_card["index"])
            return jsonify(self.player_schema.dump(original_owner))
        else:
            return (
                Forbidden(
                    description="Not allowed",
                    response=jsonify(dict(msg="Not allowed.")),
                ),
                405,
            )


class TableCardsAPI(MethodView):
    card_action_schema = CardActionSchema()
    table_schema = TableSchema()

    def post(self, table_name, current_name):
        """Give card from current_name to table"""

        current_player = players[table_name][current_name]
        give_card = self.card_action_schema.load(request.get_json())

        if give_card["signature"] == current_player.signature:
            table = tables[table_name]
            current_player.give_card_by_index(table, give_card["index"])
            return jsonify(self.table_schema.dump(table))
        else:
            return (
                Forbidden(
                    description="Not allowed",
                    response=jsonify(dict(msg="Not allowed.")),
                ),
                405,
            )

    def delete(self, table_name, current_name):
        """Take card from table to current_name"""

        current_player = players[table_name][current_name]
        take_card = self.card_action_schema.load(request.get_json())

        if take_card["signature"] == current_player.signature:
            table = tables[table_name]
            current_player.take_card_by_index(table, take_card["index"])
            return jsonify(self.table_schema.dump(table))
        else:
            return (
                Forbidden(
                    description="Not allowed",
                    response=jsonify(dict(msg="Not allowed.")),
                ),
                405,
            )


class PlayerCardActionAPI(MethodView):
    card_schema = CardSchema()
    cover_card_schema = CoverCardSchema()

    def get(self, table_name, card_owner_name, index, signature):
        """Read card by index. The card is owned by a player, self/others."""
        card_owner = players[table_name][card_owner_name]
        card = card_owner.cards[index]

        # check if card_owner equals the reader
        if signature == card_owner.signature:
            return jsonify(self.card_schema.dump(card))
        # check if card not covered
        elif not card.covered:
            return jsonify(self.card_schema.dump(card))
        else:
            return (
                Forbidden(
                    description="Not allowed",
                    response=jsonify(dict(msg="Not allowed.")),
                ),
                405,
            )

    def patch(self, table_name, card_owner_name):
        """Cover/reveal card owned by a player by its index."""
        card_owner = players[table_name][card_owner_name]

        cover_card = self.cover_card_schema.load(request.get_json())

        if cover_card["signature"] == card_owner.signature:
            card = card_owner.cards[cover_card["index"]]
            if cover_card["cover"] is True:
                card.cover(card_owner)
            elif cover_card["cover"] is False:
                card.reveal(card_owner)
            return jsonify(self.card_schema.dump(card))
        else:
            return (
                Forbidden(
                    description="Not allowed",
                    response=jsonify(dict(msg="Not allowed.")),
                ),
                405,
            )


class TableCardActionAPI(MethodView):
    card_schema = HidableCardSchema()
    cover_card_schema = CoverCardSchema()

    def get(self, table_name, index):
        table = tables[table_name]
        card = table.cards[index]

        # check if card not covered
        if not card.covered:
            return jsonify(self.card_schema.dump(card))
        else:
            return (
                Forbidden(
                    description="Not allowed",
                    response=jsonify(dict(msg="Not allowed.")),
                ),
                405,
            )

    def patch(self, table_name):
        """Cover/reveal a card by index which is owned by the table."""

        table = tables[table_name]
        cover_card = self.cover_card_schema.load(request.get_json())

        card = table.cards[cover_card["index"]]
        if cover_card["cover"] is True:
            card.cover()
        elif cover_card["cover"] is False:
            card.reveal()
        return jsonify(self.card_schema.dump(card))
