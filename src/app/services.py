from app.models import User, File

def create_user(username, password):
    user = User(username=username, password=password)
    user.save()
    return user

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def create_file(name, owner_id):
    file = File(name=name, owner_id=owner_id)
    file.save()
    return file

def get_file_by_name(name):
    return File.query.filter_by(name=name).first()
