from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])
