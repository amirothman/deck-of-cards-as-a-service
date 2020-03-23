from marshmallow import Schema, fields


class CardSchema(Schema):
    suit = fields.Str()
    number = fields.Str()
    covered = fields.Bool()
    owner = fields.Str()


class PlayerSchema(Schema):
    cards = fields.Nested(CardSchema())
    name = fields.Str()
    table_name = fields.Str()


class TableSchema(Schema):
    name = fields.Str()
    cards = fields.Nested(CardSchema())
    players = fields.Nested(PlayerSchema())
