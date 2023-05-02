from cryptography.fernet import Fernet


def generate_key():
    return Fernet.generate_key()


def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode('utf-8')).decode('utf-8')


def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')
