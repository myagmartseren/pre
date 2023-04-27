from marshmallow import Schema, fields, validate

class FileSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=128))
    description = fields.String(validate=validate.Length(max=256))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Integer(required=True)
