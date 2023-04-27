from marshmallow import ValidationError
from .file import FileSchema
from .user import UserSchema

__all__ = [
    'FileSchema',
    'UserSchema',
]

# Custom error handler for marshmallow validation errors
def handle_validation_error(error: ValidationError):
    response = {
        'message': 'Validation error occurred',
        'errors': error.messages
    }
    return response, 400
