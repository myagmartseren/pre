from marshmallow import Schema, fields

class User(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    email = fields.Str()
    public_key = fields.Str()


class File(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    capsule = fields.Str()
    path = fields.Str()
    key = fields.Str()
    
    # @pre_dump
    def pre_dump(self, obj):
        obj.name = obj.filename
        return obj
    
class Share(Schema):
    id = fields.Int(dump_only=True)
    file_id = fields.Int()
    delegator_id = fields.Int()
    delegatee_id = fields.Int()
    rekey = fields.Str(required=True)
