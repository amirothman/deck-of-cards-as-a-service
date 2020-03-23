from flask import Blueprint

from .table import TableAPI

api_blueprint = Blueprint()
api_blueprint.add_url_rule("/tables/<table_name>", view_func=TableAPI.as_view("table"))
