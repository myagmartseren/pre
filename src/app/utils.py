from cryptography.fernet import Fernet
from umbral import SecretKey
from pathlib import Path

def generate_key():
    secret_key = SecretKey.random()
    public_key = secret_key.public_key()
    return public_key, secret_key

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode('utf-8')).decode('utf-8')


def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')

OUTPUT_PATH = Path(__file__).parent

def relative_to_files(path:str) -> Path:
    ASSETS_PATH = OUTPUT_PATH / Path(r"../files")
    return ASSETS_PATH

from itsdangerous import URLSafeTimedSerializer
from flask import current_app
import jwt

from datetime import datetime, timedelta

def generate_token(user):
    current_time = datetime.utcnow()
    expiration_time = current_time + timedelta(hours=1)

    payload = {
        'user_id': user.id,
        'exp': expiration_time,
        'iat': current_time
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

    return token