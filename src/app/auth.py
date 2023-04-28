from flask import Blueprint, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'message': 'User already logged in.'}), 400

    email = request.json.get('email')
    password = request.json.get('password')
    remember_me = request.json.get('remember_me')

    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid email or password.'}), 400

    login_user(user, remember=remember_me)

    return jsonify({'message': 'Logged in successfully.'}), 200

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully.'}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify({'message': 'User already registered.'}), 400

    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    confirm_password = request.json.get('confirm_password')

    if not email or not password or not confirm_password:
        return jsonify({'message': 'Email, password, and confirm password are required.'}), 400

    if password != confirm_password:
        return jsonify({'message': 'Passwords do not match.'}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({'message': 'Email already registered.'}), 400

    password_hash = generate_password_hash(password)

    user = User(email=email, password_hash=password_hash, username=username)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.'}), 201
