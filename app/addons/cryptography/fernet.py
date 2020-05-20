from app import fernet

def encrypt(raw_data):
    raw_data = raw_data.encode()
    return fernet.encrypt(raw_data).decode('utf8')

def decrypt(encrypted_data):
    return fernet.decrypt(encrypted_data.encode()).decode('utf8')