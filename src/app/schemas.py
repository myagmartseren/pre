from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class FileSchema(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
