import os
import app
import uuid

from flask import Blueprint, jsonify, request, send_file
from flask_login import *
from app.models import User, File
import app.schemas as schemas
from app.services import *
from werkzeug.utils import secure_filename
from app.utils import relative_to_files
from app.models import db
from app.auth import login_required 

bp = Blueprint('api', __name__)


# Rest of the code...
@bp.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    return jsonify(User.dump(users, many=True))


@bp.route('/files', methods=['GET'])
@login_required
def get_files():
    user_id = current_user.id
    files = File.query.filter_by(owner_id=user_id).all()
    file_schema = schemas.File(many=True)  # Create an instance of the File schema
    return jsonify(file_schema.dump(files))  # Serialize the files using the schema

    # return jsonify(schemas.File.dump(files, many=True,obj=files))

@bp.route('/files', methods=['POST'])
@login_required
def create_file():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']

    if file.filename == '':
        return 'No file selected', 400

    generated_uuid = uuid.uuid4()
    file.save(os.path.join(app.Config.UPLOAD_FOLDER, str(relative_to_files(str(generated_uuid)))))

    name = request.form.get('name')
    key = request.form.get('key')
    capsule = request.form.get('capsule')

    new_file = File(
        name=name,
        key=bytes.fromhex(key),
        capsule=bytes.fromhex(capsule),
        path=str(generated_uuid),
        owner_id=current_user.id,
    )
    db.session.add(new_file)
    db.session.commit()

    return 'File uploaded successfully'


@bp.route('/files/<file_id>', methods=['GET'])
@login_required
def get_file(file_id):
    file = File.query.get(file_id)
    if not file:
        return jsonify({'message': 'File not found'}), 404
    file_schema = schemas.File()
    return jsonify(file_schema.dump(file))

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

@bp.route("/download/<name>")
def download_file(name):
    files = File.query.filter_by(path=name).all()
    
    return send_file(os.path.join(app.Config.UPLOAD_FOLDER, str(relative_to_files(str(name)))), as_attachment=True)