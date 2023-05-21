from app import db
from sqlalchemy.orm import backref

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(120), unique=True, nullable=False)
    lastname = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    public_key = db.Column(db.Text, unique=False, nullable=True)
    signer_key = db.Column(db.Text, unique=False, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    
    files = db.relationship('File', backref='owner', lazy=True)
    def get_id(self):
        return self.id

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    path = db.Column(db.String(256), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    key = db.Column(db.Text, unique=False, nullable=True)
    capsule = db.Column(db.Text, unique=False, nullable=True)
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

    shares = db.relationship('Share', backref='file', lazy=True)
    # @pre_dump
    def pre_dump(self, obj):
        obj.name = obj.filename
        return obj
class Share(db.Model):
    __tablename__ = 'shares'

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)
    delegator_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    delegatee_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    rekey = db.Column(db.Text, unique=False, nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(256), nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
