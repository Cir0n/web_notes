import re


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
