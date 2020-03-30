from constants import COVERED_LABEL
from models import Card, Player

from marshmallow import Schema, fields, post_load, post_dump


class CardSchema(Schema):
    suit = fields.Str()
    number = fields.Str()
    covered = fields.Bool()
    owner = fields.Str()

    @post_load
    def create_card(self, data, **kwargs):
        return Card(**data)


class HidableCardSchema(CardSchema):
    @post_dump
    def hide_cards(self, data, **kwargs):
        if data["covered"] is True:
            data["suit"] = COVERED_LABEL
            data["number"] = COVERED_LABEL
        return data


class PlayerSchema(Schema):
    cards = fields.Nested(HidableCardSchema(), many=True, dump_only=True)
    name = fields.Str()
    table_name = fields.Str(dump_only=True)
    signature = fields.Str(dump_only=True)

    @post_load
    def create_player(self, data, **kwargs):
        return Player(**data)


class TableSchema(Schema):
    name = fields.Str(dump_only=True)
    cards = fields.List(fields.Nested(HidableCardSchema()), dump_only=True)
    players = fields.List(fields.Nested(PlayerSchema()), dump_only=True)


class ActionSchema(Schema):
    signature = fields.Str()


class CardActionSchema(ActionSchema):
    index = fields.Int()


class CoverCardSchema(CardActionSchema):
    cover = fields.Bool()
