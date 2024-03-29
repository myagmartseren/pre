from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from .utils import generate_key, generate_token
from app.models import User, db
import app
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already taken'}), 400
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already taken'}), 400
    
    hashed_password = generate_password_hash(password)

    from umbral import (
    SecretKey, Signer, CapsuleFrag,
    encrypt, generate_kfrags, reencrypt, decrypt_original, decrypt_reencrypted)

    secret_key = SecretKey.random()
    public_key = secret_key.public_key()

    signing_key = SecretKey.random()
    verifying_key = signing_key.public_key()
    signer = Signer(signing_key)

    print("signing_key:",secret_key.to_secret_bytes())
    user = User(
        firstname=firstname,
        lastname=lastname, 
        email=email,
        username=username,
        password_hash=hashed_password,
        public_key=public_key.__bytes__().hex(),
        signer_key=signing_key.to_secret_bytes().hex(),
    )

    db.session.add(user)
    db.session.commit()

    access_token = generate_token(user)

    print("secret_key.__str__()",str(secret_key))
    return jsonify({
        'id': user.id,
        'username': user.username,
        'public_key': user.public_key,
        "private_key":secret_key.to_secret_bytes().hex(),
        'access_token': access_token
    })


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    login_user(user)

    access_token = generate_token(user)

    print("login fucking id",user.id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'public_key': user.public_key,
        'access_token': access_token
    })

@bp.route('/logout', methods=['POST'])
def logout():
    # Log out the current user
    logout_user()
    return jsonify({'message': 'Logged out successfully'})


from functools import wraps
from flask import current_app

# Define the user_loader callback function
@app.login_manager.user_loader
def load_user(user_id):
    # Retrieve the user object based on the user_id
    # Return the user object or None if not found
    return User.query.get(user_id)


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
