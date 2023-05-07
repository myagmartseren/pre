from cryptography.fernet import Fernet
from umbral import SecretKey

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
