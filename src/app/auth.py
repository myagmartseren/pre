from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User
from app.models import db
from .utils import generate_key

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
        return jsonify({'error': 'email already taken'}), 400
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'email already taken'}), 400
    
    hashed_password = generate_password_hash(password)
    public_key, secret_key = generate_key()
    signer_key, _ = generate_key()
    
    user = User(
        firstname=firstname,
        lastname=lastname, 
        email= email,
        username = username,
        password_hash = hashed_password,
        public_key = public_key.__bytes__(),
        signer_key = signer_key.__bytes__(),
    )

    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'private_key': secret_key.to_secret_bytes().hex()})


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid username or password'}), 401
    return jsonify({"username":user.username})
