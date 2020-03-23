from flask import jsonify
from flask.views import MethodView

from models.table import Table
from schemas import TableSchema

tables = {}


class TableAPI(MethodView):
    def get(self, table_name):
        # get table
        pass

    def post(self):
        # create a new table
        table = Table()
        tables[table.name] = table
        return jsonify(TableSchema.dump(table))
