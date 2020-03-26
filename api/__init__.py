from flask import Blueprint

from .endpoints import (
    TableAPI,
    PlayerAPI,
    PlayersCardsAPI,
    TableCardsAPI,
    ReadPlayerCardAPI,
    ReadTableCardAPI,
)

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

table_view = TableAPI.as_view("table")
api_blueprint.add_url_rule("/table/<table_name>", view_func=table_view, methods=["GET"])
api_blueprint.add_url_rule("/table", view_func=table_view, methods=["POST"])


player_view = PlayerAPI.as_view("player")
api_blueprint.add_url_rule(
    "/table/<table_name>/players", view_func=player_view, methods=["POST"]
)
api_blueprint.add_url_rule(
    "/table/<table_name>/players/<player_name>", view_func=player_view, methods=["GET"]
)

players_cards_view = PlayersCardsAPI.as_view("players_cards")
api_blueprint.add_url_rule(
    "/table/<table_name>/players/<current_name>/cards/<other_name>",
    view_func=players_cards_view,
)

table_cards_view = TableCardsAPI.as_view("table_cards")
api_blueprint.add_url_rule(
    "/table/<table_name>/players/<current_name>/table", view_func=table_cards_view
)

read_table_card_view = ReadTableCardAPI.as_view("table_card")
api_blueprint.add_url_rule(
    "/table/<table_name>/card/<index>", view_func=read_table_card_view,
)

read_player_card_view = ReadPlayerCardAPI.as_view("player_card")
api_blueprint.add_url_rule(
    "/table/<table_name>/player/<card_owner_name>/card/<index>/<signature>",
    view_func=read_player_card_view,
)
