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

def grant_access(file_id, user_id):
    access = Access(file_id=file_id, user_id=user_id)
    access.save()
    return access

def revoke_access(file_id, user_id):
    access = Access.query.filter_by(file_id=file_id, user_id=user_id).first()
    if access:
        access.delete()

def get_file_owners(file_id):
    owners = []
    file = File.query.get(file_id)
    owners.append(file.owner_id)
    access_list = Access.query.filter_by(file_id=file_id).all()
    for access in access_list:
        owners.append(access.user_id)
    return owners
