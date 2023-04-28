from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    path = db.Column(db.String(256), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'path': self.path,
            'type':self.type
        }

class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delegator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    delegatee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    re_key = db.Column(db.String(256), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'delegator_id': self.delegator_id,
            'delegatee_id': self.delegatee_id,
            'file_id': self.file_id,
            'is_active':self.is_active,
            're_key':self.re_key,
        }

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    action = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime(timezone=True),server_default=db.func.now(), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.filename,
            'path': self.filepath,
            'type':self.type
        }

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    public_key = db.Column(db.String(128), nullable=True)
    private_key = db.Column(db.String(128), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'public_key':self.public_key
        }

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
