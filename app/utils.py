import hashlib
import hmac
import re

from app.extensions import CIPHER, HMAC_KEY


def is_valid_name(name):
    return bool(re.match(r"^[a-zA-Z ]+$", name))


def is_valid_username(username):
    return bool(re.match(r"^[a-zA-Z0-9]+$", username))


def is_valid_grade(grade):
    try:
        grade = float(grade)
        return 0 <= grade <= 20
    except ValueError:
        return False


def is_valid_password(password):
    return len(password) >= 8


def encrypt_data(data):
    return CIPHER.encrypt(data.encode()).decode()


def decrypt_data(data):
    return CIPHER.decrypt(data.encode()).decode()


def hash_username(username):
    return hmac.new(HMAC_KEY, username.encode(), hashlib.sha256).hexdigest()
