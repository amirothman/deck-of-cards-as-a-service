from models import Card, Player, Table

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
    cards = fields.Nested(CardSchema(), many=True)
    name = fields.Str()
    table_name = fields.Str()
    signature = fields.Str()

    @post_load
    def create_player(self, data, **kwargs):
        return Player(**data)


class TableSchema(Schema):
    name = fields.Str()
    cards = fields.Nested(CardSchema(), many=True)
    players = fields.Nested(PlayerSchema(), many=True)

    @post_load
    def create_table(self, data, **kwargs):
        return Table(**data)
