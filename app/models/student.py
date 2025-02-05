from app.config import Database


class StudentModel:
    def __init__(self):
        self.db = Database()

    def get_student_by_id(self, student_id):
        query = """SELECT id, first_name, last_name, class_id FROM students
                    WHERE id = %s"""
        result = self.db.query(
            query, (student_id,)
        )  # Exécute la requête normalement
        return result[0] if result else None

    def get_all_students(self):
        sql = """
        SELECT s.id, s.first_name, s.last_name, c.name AS class_name,
            GROUP_CONCAT(DISTINCT sub.name SEPARATOR ', ') AS subjects
        FROM students s
        LEFT JOIN class c ON s.class_id = c.id
        LEFT JOIN student_subject ss ON s.id = ss.student_id
        LEFT JOIN subjects sub ON ss.subject_id = sub.id
        GROUP BY s.id, s.first_name, s.last_name, c.name
        """
        return self.db.query(sql)

    def create_student(
        self,
        user_id,
        first_name,
        last_name,
        class_id,
        selected_languages,
        selected_options,
    ):
        query = """INSERT INTO students ( id, first_name, last_name, class_id)
                VALUES (%s, %s, %s, %s)"""
        self.db.execute(query, (user_id, first_name, last_name, class_id))

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
        query = """
        SELECT id, first_name, last_name
        From students
        WHERE class_id = %s
        """
        return self.db.query(query, (class_id,))

    def delete_student(self, student_id):
        query = "DELETE FROM users WHERE id = %s"
        self.db.execute(query, (student_id,))

    def get_student_subject(self, student_id):
        query = """
        SELECT s.id, s.name, s.type
        FROM subjects s
        JOIN student_subject ss ON s.id = ss.subject_id
        WHERE ss.student_id = %s
        """
        return self.db.query(query, (student_id,))

    def get_subject_by_id(self, subject_id):
        query = "SELECT id, name, type FROM subjects WHERE id = %s"
        result = self.db.query(query, (subject_id,))
        return result[0] if result else None
