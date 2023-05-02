import os
from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import File

files_bp = Blueprint('files', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@files_bp.route('/files', methods=['GET'])
@login_required
def get_files():
    files = File.query.filter_by(user_id=current_user.id).all()
    return jsonify([file.to_dict() for file in files])

@files_bp.route('/files', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file uploaded.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        new_file = File(user_id=current_user.id, filename=filename, filepath=filepath)
        db.session.add(new_file)
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully.'}), 201
    else:
        return jsonify({'error': 'Invalid file type.'}), 400
