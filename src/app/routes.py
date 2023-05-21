from flask import Blueprint, jsonify, request
from app.models import User, File
import app.schemas as schemas
from app.services import *

bp = Blueprint('api', __name__)

@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(User.dump(users, many=True))


@bp.route('/files', methods=['GET'])
def get_files():
    files = File.query.all()
    return jsonify(schemas.File.dump(files, many=True))


@bp.route('/files', methods=['POST'])
def create_file():
    # Get file info from request
    name = request.form['name']
    owner_id = request.form['owner_id']

    # Create new file and add it to the database
    file = File(name=name, content=content, owner_id=owner_id)
    create_file(file)

    return jsonify(schemas.File.dump(file))


@bp.route('/files/<file_id>', methods=['GET'])
def get_file(file_id):
    file = get_file(file_id)

    if not file:
        return jsonify({'message': 'File not found'}), 404

    return jsonify(schemas.File.dump(file))


@bp.route('/files/<file_id>', methods=['PUT'])
def update_file(file_id):
    # Get file info from request
    data = request.get_json()
    name = data.get('name')
    content = data.get('content')

    # Update the file and save changes to the database
    file = update_file(file_id, name=name, content=content)

    if not file:
        return jsonify({'message': 'File not found'}), 404

    return jsonify(schemas.File.dump(file))


@bp.route('/files/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    delete_file(file_id)

    return '', 204
