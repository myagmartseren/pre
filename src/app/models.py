from app import db
from sqlalchemy.orm import backref

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    public_key = db.Column(db.LargeBinary, unique=False, nullable=True)
    private_key = db.Column(db.LargeBinary, unique=False, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    files = db.relationship('File', backref='owner', lazy=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    path = db.Column(db.String(256), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    shares = db.relationship('Share', backref='file', lazy=True)

class Share(db.Model):
    __tablename__ = 'shares'

    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), nullable=False)
    delegator_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    delegatee_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    re_key = db.Column(db.String(256), nullable=False)
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
