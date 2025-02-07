from app import bcrypt
from app.config import Database
from app.utils import decrypt_data, encrypt_data, hash_username


class UserModel:
    def __init__(self):
        self.db = Database()

    def add_user(self, username, password, role):
        hashed_password = bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )
        encrypted_username = encrypt_data(username)
        hmac_username = hash_username(username)
        sql = """INSERT INTO users (username, password, role, hmac_username)
        VALUES (%s, %s, %s, %s)"""
        self.db.execute(
            sql, (encrypted_username, hashed_password, role, hmac_username)
        )
        return self.db.cursor.lastrowid  # id user

    def get_user_by_username(self, username):
        hmac_username = hash_username(username)

        sql = "SELECT * FROM users WHERE hmac_username = %s"
        result = self.db.query(sql, (hmac_username,))
        print(result)
        if result:
            user = result[0]
            user["username"] = decrypt_data(user["username"])
            return user
        return None

    def check_password(self, username, password):
        user = self.get_user_by_username(username)
        if user and bcrypt.check_password_hash(user["password"], password):
            return True
        return False

    def add_admin(self, username, password):
        return self.add_user(username, password, role="admin")
