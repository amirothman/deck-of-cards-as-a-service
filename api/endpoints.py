from collections import defaultdict

from flask import jsonify, request
from flask.views import MethodView

from models.table import Table
from schemas import TableSchema, PlayerSchema

tables = {}
players = defaultdict(dict)


class TableAPI(MethodView):
    def get(self, table_name):
        # get table
        table = tables[table_name]
        dump = TableSchema().dump(table)
        return jsonify(dump)


class ListTableAPI(MethodView):
    def post(self):
        # create a new table
        table = Table()
        tables[table.name] = table
        dump = TableSchema().dump(table)
        return jsonify(dump)


class ListPlayerAPI(MethodView):
    schema = PlayerSchema()

    def get(self, table_name):
        return jsonify(self.schema.dump(players[table_name].values(), many=True))

    def post(self, table_name):
        player = self.schema.load(request.get_json())

        # join the table
        player.join_table(tables[table_name])

        # persist to memory
        players[table_name][player.name] = player

        return jsonify(self.schema.dump(player))
