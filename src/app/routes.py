from flask import Blueprint, jsonify, request
from flask_login import *
from app.models import User, File
import app.schemas as schemas
from app.services import *
from werkzeug.utils import secure_filename
import app
import os
from app.utils import relative_to_files
import uuid
from app.models import db
from functools import wraps

bp = Blueprint('api', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = None

        if 'Authorization' in request.headers:
            header_value = request.headers['Authorization']
            access_token = header_value.split(' ')[-1]

        if not access_token:
            print('Missing access token')
            return 'Missing access token', 401

        user = verify_access_token(access_token)
        if not user:
            print('Invalid access token')
            return 'Invalid access token', 401

        login_user(user)

        return f(*args, **kwargs)

    return decorated_function

from flask import current_app

def verify_access_token(access_token):
    # Implement your access token verification logic here
    # For example, decode the access token and validate it against a stored token
    # Retrieve the user based on the access token and return it
    # If the access token is invalid or expired, return None

    if not access_token:
        print("accees_token none")
        return None

    # Sample implementation:
    # Decode the access token
    decoded_token = decode_access_token(access_token,current_app.config['SECRET_KEY'])

    if decoded_token is None:
        print("decoded_token none")
        return None

    # Check if the token is valid and not expired
    if is_token_valid(decoded_token):
        # Retrieve the user based on the token data
        user_id = decoded_token.get('user_id')
        user = User.query.get(user_id)
        return user
    
    print("accees_token none 2")
    return None


# Rest of the code...

@bp.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    return jsonify(User.dump(users, many=True))


@bp.route('/files', methods=['GET'])
@login_required
def get_files():
    files = File.query.all()
    return jsonify(schemas.File.dump(files, many=True))


@bp.route('/files', methods=['POST'])
@login_required
def create_file():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']

    if file.filename == '':
        return 'No file selected', 400

    filename = secure_filename(file.filename)
    generated_uuid = uuid.uuid4()
    relative_path = relative_to_files(str(generated_uuid))
    file.save(os.path.join(app.Config.UPLOAD_FOLDER, str(generated_uuid)))

    name = request.form.get('name')
    key = request.form.get('key')
    capsule = request.form.get('capsule')

    new_file = File(
        name=filename,
        key=key,
        capsule=capsule,
        path=relative_path,
        owner_id=current_user.id,
    )
    db.session.add(new_file)
    db.session.commit()

    return 'File uploaded successfully'


@bp.route('/files/<file_id>', methods=['GET'])
@login_required
def get_file(file_id):
    file = get_file(file_id)

    if not file:
        return jsonify({'message': 'File not found'}), 404

    return jsonify(schemas.File.dump(file))


@bp.route('/files/<file_id>', methods=['PUT'])
@login_required
def update_file(file_id):
    data = request.get_json()
    name = data.get('name')
    content = data.get('content')

    file = update_file(file_id, name=name, content=content)

    if not file:
        return jsonify({'message': 'File not found'}), 404

    return jsonify(schemas.File.dump(file))


@bp.route('/files/<file_id>', methods=['DELETE'])
@login_required
def delete_file(file_id):
    delete_file(file_id)

    return '', 204


import jwt
from datetime import datetime, timedelta

def decode_access_token(access_token, secret_key):
    if access_token is None:
        raise ValueError("access_token cannot be None")

    try:
        decoded_token = jwt.decode(access_token, secret_key, algorithms=['HS256'])
        print("value", decoded_token)
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("ExpiredSignatureError")
        # Handle expired token
        return None
    except jwt.InvalidTokenError:
        print("InvalidTokenError")
        # Handle invalid token
        return None

def is_token_valid(decoded_token):
    if decoded_token is None:
        print("is_token_valid decoded_token none")
        return False

    expiration_timestamp = decoded_token.get('exp')
    if expiration_timestamp is None:
        print("is_token_valid expiration_timestamp none")
        return False

    current_timestamp = datetime.utcnow().timestamp()
    if current_timestamp >= expiration_timestamp:
        # Token has expired
        print("Token has expired")
        return False

    return True
