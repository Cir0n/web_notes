from app.models.grade import GradeModel
from app.models.student import StudentModel
from app.models.teacher import TeacherModel
from app.models.user import UserModel
from app.utils import (
    is_valid_grade,
    is_valid_name,
    is_valid_password,
    is_valid_username,
)


class TeacherController:
    def __init__(self):
        self.teacher_model = TeacherModel()
        self.user_model = UserModel()
        self.grade_model = GradeModel()
        self.student_model = StudentModel()

    def get_teacher(self, teacher_id):
        teacher = self.teacher_model.get_teacher_by_id(teacher_id)
        if not teacher:
            return "ERROR: Teacher not found"
        return teacher

    def list_teachers(self):
        return self.teacher_model.get_all_teachers()

    def edit_teacher(
        self,
        teacher_id,
        first_name,
        last_name,
        class_id,
        selected_languages,
        selected_options,
    ):
        self.teacher_model.edit_teacher(
            teacher_id,
            first_name,
            last_name,
            class_id,
            selected_languages,
            selected_options,
        )

        return "Success: Teacher updated successfully"

    def create_teacher(
        self, username, password, first_name, last_name, class_ids, subject_ids
    ):
        if not is_valid_name(first_name) or not is_valid_name(last_name):
            return {
                "error": """Le prénom et le nom ne doivent contenir que
                    des lettres"""
            }

        if not is_valid_username(username):
            return {
                "error": """Le nom d'utilisateur doit contenir que des lettres,
                chiffres et underscores."""
            }

        if not is_valid_password(password):
            return {
                "error": """Le mot de passe doit contenir au moins
                    8 caractères"""
            }

        if self.user_model.get_user_by_username(username):
            return {"error": "Le nom d'utilisateur est déjà utilisé"}

        user_id = self.user_model.add_user(username, password, role="teacher")
        self.teacher_model.create_teacher(
            user_id, first_name, last_name, class_ids, subject_ids
        )
        return "Success: Teacher created successfully"

    def delete_teacher(self, teacher_id):
        self.teacher_model.delete_teacher(teacher_id)

    def add_grade(self, teacher_id, student_id, subject_id, grade, comment=""):
        if not is_valid_grade(grade):
            return {"error: Les notes doivent être un nombre entre 0 et 20"}

        self.grade_model.add_grade(
            teacher_id, student_id, subject_id, grade, comment
        )

    def get_student_grades(self, teacher_id, student_id):
        return self.grade_model.get_student_grades(teacher_id, student_id)

    def get_student_classes(self, class_id):
        return self.student_model.get_student_classes(class_id)

    def get_teacher_classes(self, teacher_id):
        return self.teacher_model.get_teacher_classes(teacher_id)

    def get_teacher_subjects(self, teacher_id):
        return self.teacher_model.get_teacher_by_subject(teacher_id)

    def delete_grade(self, teacher_id, grade_id):
        return self.grade_model.delete_grade(teacher_id, grade_id)
