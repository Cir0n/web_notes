from app import bcrypt
from app.config import Database


class UserModel:
    def __init__(self):
        self.db = Database()

    def add_user(self, username, password, role):
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        sql = """INSERT INTO users (username, password, role)
        VALUES (%s, %s, %s)"""
        self.db.execute(sql, (username, hashed_password, role))
        return self.db.cursor.lastrowid  # id user

    def get_user_by_username(self, username):
        sql = "SELECT * FROM users WHERE username = %s"
        result = self.db.query(sql, (username,))
        return result[0] if result else None

    def check_password(self, username, password):
        user = self.get_user_by_username(username)
        if user and bcrypt.check_password_hash(user["password"], password):
            return True
        return False

    def add_admin(self, username, password):
        return self.add_user(username, password, role="admin")
