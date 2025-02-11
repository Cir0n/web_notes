from app.models.grade import GradeModel
from app.models.student import StudentModel
from app.models.user import UserModel
from app.utils import is_valid_name, is_valid_password, is_valid_username


class StudentController:
    """
    StudentController handles the logic for student-related operations.
    """

    def __init__(self):
        """
        Initializes the StudentController with the necessary models.
        """
        self.model = StudentModel()
        self.user_model = UserModel()
        self.grade_model = GradeModel()

    def get_student_info(self, student_id):
        """
        Retrieves a student by their ID.

        :param student_id: The ID of the student.
        :return: A dictionary containing student details or an error message.
        """
        student = self.model.get_student_by_id(student_id)
        if not student:
            return "ERROR: Student not found"
        return student

    def list_students(self):
        """
        Retrieves all students.

        :return: A list of dictionaries containing student details.
        """
        return self.model.get_all_students()

    def create_student(
        self,
        username,
        password,
        first_name,
        last_name,
        class_id,
        selected_languages,
        selected_options,
    ):
        """
        Creates a new student.

        :param username: The username of the student.
        :param password: The password of the student.
        :param first_name: The first name of the student.
        :param last_name: The last name of the student.
        :param class_id: The ID of the class the student belongs to.
        :param selected_languages: A list of selected language subject IDs.
        :param selected_options: A list of selected optional subject IDs.
        :return: A success message or an error message.
        """
        if not is_valid_name(first_name):
            return {"error": "Le prenom doit contenir que des lettres"}

        if not is_valid_username(username):
            return {
                "error": """Le nom d'utilisateur doit contenir que des lettre,
                chiffre et underscores."""
            }

        if not is_valid_password(password):
            return {
                "error": """Le mot de passe doit contenir au moins
                    8 caractères"""
            }

        if self.user_model.get_user_by_username(username):
            return {"error": "Le nom d'utilisateur est déjà utilisé"}

        user_id = self.user_model.add_user(username, password, role="student")
        self.model.create_student(
            user_id,
            first_name,
            last_name,
            class_id,
            selected_languages,
            selected_options,
        )

        return "Success: Student created successfully"

    def delete_student(self, student_id):
        """
        Deletes a student by their ID.

        :param student_id: The ID of the student to be deleted.
        """
        self.model.delete_student(student_id)

    def get_student_grades(self, student_id):
        """
        Retrieves all grades for a specific student.

        :param student_id: The ID of the student.
        :return: A list of grades.
        """
        grades = self.grade_model.get_student_grade_by_student(student_id)
        return grades if grades else []

    def get_student_subject(self, student_id):
        """
        Retrieves all subjects for a specific student.

        :param student_id: The ID of the student.
        :return: A list of subjects.
        """
        subjects = self.model.get_student_subject(student_id)
        return subjects if subjects else []

    def get_student_grades_by_subject(self, student_id, subject_id):
        """
        Retrieves all grades for a specific student in a specific subject.

        :param student_id: The ID of the student.
        :param subject_id: The ID of the subject.
        :return: A list of grades.
        """
        grades = self.grade_model.get_student_grades_by_subject(
            student_id, subject_id
        )
        return grades if grades else []

    def get_subject_info(self, subject_id):
        """
        Retrieves a subject by its ID.

        :param subject_id: The ID of the subject.
        :return: A dictionary containing subject details.
        """
        subject = self.model.get_subject_by_id(subject_id)
        return subject
