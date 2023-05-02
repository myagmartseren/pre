from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User
from app.models import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint for registering a new user.
    Expects a JSON payload with the following fields:
    - username
    - password
    Returns a JSON object with the newly created user's ID and username.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already taken'}), 400
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username})


@bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user authentication.
    Expects a JSON payload with the following fields:
    - username
    - password
    Returns a JSON object with the authenticated user's ID and username.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401
    return jsonify({'id': user.id, 'username': user.username})
