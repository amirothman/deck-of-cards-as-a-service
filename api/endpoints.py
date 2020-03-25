from collections import defaultdict

from flask import jsonify, request
from flask.views import MethodView

from models.table import Table

from schemas import TableSchema, PlayerSchema, MoveCardSchema

tables = {}
players = defaultdict(dict)


class TableAPI(MethodView):
    def get(self, table_name):
        # get table
        table = tables[table_name]

        dump = TableSchema().dump(table)
        return jsonify(dump)

    def post(self):
        # create a new table
        table = Table()
        tables[table.name] = table

        dump = TableSchema().dump(table)
        return jsonify(dump)


class PlayerAPI(MethodView):
    schema = PlayerSchema()

    def get(self, table_name, player_name):
        if player_name:
            return jsonify(self.schema.dump(players[table_name][player_name]))

        return jsonify(self.schema.dump(players[table_name].values(), many=True))

    def post(self, table_name):
        player = self.schema.load(request.get_json())

        # join the table
        player.join_table(tables[table_name])

        # persist to memory
        players[table_name][player.name] = player

        return jsonify(self.schema.dump(player))


class PlayersCardsAPI(MethodView):
    move_card_schema = MoveCardSchema()
    player_schema = PlayerSchema()

    def post(self, table_name, current_name, other_name):
        """Give card from current_name to other_name"""

        current_player = players[table_name][current_name]
        give_card = self.move_card_schema.load(request.get_json())

        if give_card["signature"] == current_player.signature:
            recepient = players[table_name][other_name]
            current_player.give_card_by_index(recepient, give_card["index"])
            return jsonify(self.player_schema.dump(recepient))
        else:
            raise Exception("Not allowed")

    def delete(self, table_name, current_name, other_name):
        """Take card from other_name to current_name"""

        current_player = players[table_name][current_name]
        take_card = self.move_card_schema.load(request.get_json())

        if take_card["signature"] == current_player.signature:
            original_owner = players[table_name][other_name]
            current_player.take_card_by_index(original_owner, take_card["index"])
            return jsonify(self.player_schema.dump(original_owner))
        else:
            raise Exception("Not allowed")


class TableCardsAPI(MethodView):
    move_card_schema = MoveCardSchema()
    table_schema = TableSchema()

    def post(self, table_name, current_name):
        """Give card from current_name to table"""

        current_player = players[table_name][current_name]
        give_card = self.move_card_schema.load(request.get_json())

        if give_card["signature"] == current_player.signature:
            table = tables[table_name]
            current_player.give_card_by_index(table, give_card["index"])
            return jsonify(self.table_schema.dump(table))
        else:
            raise Exception("Not allowed")

    def delete(self, table_name, current_name):
        """Take card from table to current_name"""

        current_player = players[table_name][current_name]
        take_card = self.move_card_schema.load(request.get_json())

        if take_card["signature"] == current_player.signature:
            table = tables[table_name]
            current_player.take_card_by_index(table, take_card["index"])
            return jsonify(self.table_schema.dump(table))
        else:
            raise Exception("Not allowed")
