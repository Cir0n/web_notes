from flask import session

from app.models.student import StudentModel
from app.models.teacher import TeacherModel
from app.models.user import UserModel


class AuthController:
    def __init__(self):
        self.user_model = UserModel()
        self.student_model = StudentModel()
        self.teacher_model = TeacherModel()

    def login(self, username, password):
        user = self.user_model.get_user_by_username(username)
        if user and self.user_model.check_password(username, password):
            session["user_id"] = user["id"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return {"success": "Login successful", "role": user["role"]}

            return {"success": "Login successful", "role": user["role"]}
        return {"error": "Invalid username or password"}

    def logout(self):
        session.clear()
        return {"success": "Logout successful"}
