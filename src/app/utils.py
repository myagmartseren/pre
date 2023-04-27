import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_uuid():
    return str(uuid.uuid4())

def save_file(file, upload_folder):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        uuid_filename = generate_uuid() + '.' + filename.rsplit('.', 1)[1].lower()
        file_path = os.path.join(upload_folder, uuid_filename)
        file.save(file_path)
        return uuid_filename
    else:
        return None
