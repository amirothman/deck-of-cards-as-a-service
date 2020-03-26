from models import Card, Player

from marshmallow import Schema, fields, post_load


class CardSchema(Schema):
    suit = fields.Str()
    number = fields.Str()
    covered = fields.Bool()
    owner = fields.Str()

    @post_load
    def create_card(self, data, **kwargs):
        return Card(**data)


class PlayerSchema(Schema):
    cards = fields.Nested(CardSchema(), many=True, dump_only=True)
    name = fields.Str()
    table_name = fields.Str(dump_only=True)
    signature = fields.Str(dump_only=True)

    @post_load
    def create_player(self, data, **kwargs):
        return Player(**data)


class TableSchema(Schema):
    name = fields.Str(dump_only=True)
    cards = fields.List(fields.Nested(CardSchema()), dump_only=True)
    players = fields.List(fields.Nested(PlayerSchema()), dump_only=True)


class CardActionSchema(Schema):
    signature = fields.Str()
    index = fields.Int()
