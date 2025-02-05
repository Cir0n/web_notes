from app.config import Database


class TeacherModel:
    def __init__(self):
        self.db = Database()

    def create_teacher(
        self, user_id, first_name, last_name, class_ids, subject_ids
    ):
        query = """INSERT INTO teachers ( id, first_name, last_name)
        VALUES (%s, %s, %s)"""
        self.db.execute(query, (user_id, first_name, last_name))

        if class_ids:
            for class_id in class_ids:
                query = """INSERT INTO teacher_class (teacher_id, class_id)
                    VALUES (%s, %s)"""
                self.db.execute(query, (user_id, class_id))

        if subject_ids:
            for subject_id in subject_ids:
                query = """INSERT INTO teacher_subject (teacher_id, subject_id)
                VALUES (%s, %s)"""
                self.db.execute(query, (user_id, subject_id))
        return user_id

    def get_all_teachers(self):
        query = """
        SELECT t.id, t.first_name, t.last_name,
            GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') AS classes,
            GROUP_CONCAT(DISTINCT s.name SEPARATOR ', ') AS subjects
        FROM teachers t
        LEFT JOIN teacher_class tc ON t.id = tc.teacher_id
        LEFT JOIN class c ON tc.class_id = c.id
        LEFT JOIN teacher_subject ts ON t.id = ts.teacher_id
        LEFT JOIN subjects s ON ts.subject_id = s.id
        GROUP BY t.id
        """
        return self.db.query(query)

    def get_teacher_by_id(self, teacher_id):
        query = "SELECT * FROM teachers WHERE id = %s"
        result = self.db.query(query, (teacher_id,))
        return result[0] if result else None

    def delete_teacher(self, teacher_id):
        query = "DELETE FROM users WHERE id = %s"
        self.db.execute(query, (teacher_id,))

    def get_teacher_classes(self, teacher_id):
        query = """
        SELECT c.id, c.name
        FROM class c
        JOIN teacher_class tc ON c.id = tc.class_id
        WHERE tc.teacher_id = %s
        """
        return self.db.query(query, (teacher_id,))

    def get_teacher_by_subject(self, teacher_id):
        query = """
        SELECT s.id, s.name
        FROM subjects s
        JOIN teacher_subject ts ON s.id = ts.subject_id
        WHERE ts.teacher_id = %s
        """
        return self.db.query(query, (teacher_id,))
