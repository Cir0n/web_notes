from app.config import Database
from app.utils import decrypt_data, encrypt_data


class StudentModel:
    """
    StudentModel handles database operations related to the 'students' table.
    """

    def __init__(self):
        """
        Initializes the StudentModel with a database connection.
        """
        self.db = Database()

    def get_student_by_id(self, student_id):
        """
        Retrieves a student by their ID.

        :param student_id: The ID of the student.
        :return: A dictionary containing student details or None if not found.
        """
        query = """SELECT id, first_name, last_name, class_id FROM students
                    WHERE id = %s"""
        result = self.db.query(query, (student_id,))
        return result[0] if result else None

    def get_all_students(self):
        """
        Retrieves all students from the database.

        :return: A list of dictionaries containing student details.
        """
        query = """
        SELECT s.id, s.first_name, s.last_name, c.name AS class_name,
            GROUP_CONCAT(DISTINCT sub.name SEPARATOR ', ') AS subjects
        FROM students s
        LEFT JOIN class c ON s.class_id = c.id
        LEFT JOIN student_subject ss ON s.id = ss.student_id
        LEFT JOIN subjects sub ON ss.subject_id = sub.id
        GROUP BY s.id, s.first_name, s.last_name, c.name
        """
        result = self.db.query(query)

        # Vérifier les données brutes récupérées
        print("Données récupérées depuis la base :", result)

        for student in result:
            student["first_name"] = decrypt_data(student["first_name"])
            student["last_name"] = decrypt_data(student["last_name"])
        return result

    def create_student(
        self,
        user_id,
        first_name,
        last_name,
        class_id,
        selected_languages,
        selected_options,
    ):
        """
        Creates a new student in the database.

        :param user_id: The ID of the user.
        :param first_name: The first name of the student.
        :param last_name: The last name of the student.
        :param class_id: The ID of the class the student belongs to.
        :param selected_languages: A list of selected language subject IDs.
        :param selected_options: A list of selected optional subject IDs.
        :return: The user ID of the created student.
        """
        encrypted_fist_name = encrypt_data(first_name)
        encrypted_last_name = encrypt_data(last_name)
        query = """INSERT INTO students ( id, first_name, last_name, class_id)
                VALUES (%s, %s, %s, %s)"""
        self.db.execute(
            query,
            (user_id, encrypted_fist_name, encrypted_last_name, class_id),
        )

        sql_principal_subject = """Select id from subjects
        where type = 'Principal'
        """
        principal_subjects = self.db.query(sql_principal_subject)
        for subject in principal_subjects:
            query = """INSERT INTO student_subject (student_id, subject_id)
                     VALUES (%s, %s)"""
            self.db.execute(query, (user_id, subject["id"]))

        for language in selected_languages:
            query = """INSERT INTO student_subject (student_id, subject_id)
                    VALUES (%s, %s)"""
            self.db.execute(query, (user_id, language))

        for option in selected_options:
            query = """INSERT INTO student_subject (student_id, subject_id)
                    VALUES (%s, %s)"""
            self.db.execute(query, (user_id, option))

        return user_id

    def get_student_classes(self, class_id):
        """
        Retrieves all students in a specific class.

        :param class_id: The ID of the class.
        :return: A list of dictionaries containing student details.
        """
        query = """
        SELECT id, first_name, last_name
        From students
        WHERE class_id = %s
        """
        students = self.db.query(query, (class_id,))
        for student in students:
            student["first_name"] = decrypt_data(student["first_name"])
            student["last_name"] = decrypt_data(student["last_name"])
        return students

    def delete_student(self, student_id):
        """
        Deletes a student from the database.

        :param student_id: The ID of the student to be deleted.
        """
        query = "DELETE FROM users WHERE id = %s"
        self.db.execute(query, (student_id,))

    def get_student_subject(self, student_id):
        """
        Retrieves all subjects for a specific student.

        :param student_id: The ID of the student.
        :return: A list of dictionaries containing subject details.
        """
        query = """
        SELECT s.id, s.name, s.type
        FROM subjects s
        JOIN student_subject ss ON s.id = ss.subject_id
        WHERE ss.student_id = %s
        """
        return self.db.query(query, (student_id,))

    def get_subject_by_id(self, subject_id):
        """
        Retrieves a subject by its ID.

        :param subject_id: The ID of the subject.
        :return: A dictionary containing subject details or None if not found.
        """
        query = "SELECT id, name, type FROM subjects WHERE id = %s"
        result = self.db.query(query, (subject_id,))
        if result:
            student = result[0]
            student["first_name"] = decrypt_data(student["first_name"])
            student["last_name"] = decrypt_data(student["last_name"])
            return student
