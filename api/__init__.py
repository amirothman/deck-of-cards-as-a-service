from flask import Blueprint

from .endpoints import TableAPI, ListTableAPI, ListPlayerAPI

api_blueprint = Blueprint("api", __name__)
api_blueprint.add_url_rule("/table/<table_name>", view_func=TableAPI.as_view("table"))
api_blueprint.add_url_rule("/table", view_func=ListTableAPI.as_view("list_table"))
api_blueprint.add_url_rule(
    "/table/<table_name>/players", view_func=ListPlayerAPI.as_view("list_player")
)
