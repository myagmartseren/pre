from marshmallow import Schema, fields

class User(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    firstname = fields.Str()
    lastname = fields.Str()
    email = fields.Str()

class File(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
