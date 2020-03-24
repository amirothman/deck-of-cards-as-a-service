from models import Card, Player, Table

from marshmallow import Schema, fields, post_load


class CardSchema(Schema):
    suit = fields.Str(load_only=True)
    number = fields.Str(load_only=True)
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
    name = fields.Str()
    cards = fields.List(fields.Nested(CardSchema()), allow_none=True)
    players = fields.List(fields.Nested(PlayerSchema()), allow_none=True)

    @post_load
    def create_table(self, data, **kwargs):
        table = Table()
        return table


class MoveCardSchema(Schema):
    signature = fields.Str()
    index = fields.Int()
