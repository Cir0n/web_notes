from app.config import Database


class GradeModel:
    """
    GradeModel handles database operations related to the 'grades' table.
    """

    def __init__(self):
        """
        Initializes the GradeModel with a database connection.
        """
        self.db = Database()

    def add_grade(self, teacher_id, student_id, subject_id, grade, comment=""):
        """
        Adds a new grade to the database.

        :param teacher_id: The ID of the teacher assigning the grade.
        :param student_id: The ID of the student receiving the grade.
        :param subject_id: The ID of the subject for which the grade
        is assigned.
        :param grade: The grade value.
        :param comment: Optional comment about the grade.
        :return: The result of the database execution.
        """
        query = """INSERT INTO grades (teacher_id, student_id, subject_id,
        grade, comment)
        VALUES (%s, %s, %s, %s, %s)"""
        return self.db.execute(
            query, (teacher_id, student_id, subject_id, grade, comment)
        )

    def get_student_grades(self, teacher_id, student_id):
        """
        Retrieves all grades for a specific student assigned by a specific
        teacher.

        :param teacher_id: The ID of the teacher.
        :param student_id: The ID of the student.
        :return: A list of grades.
        """
        query = """
        SELECT g.id, g.grade, g.comment, g.created_at AS
        date_added, sub.name AS subject_name
        FROM grades g
        JOIN subjects sub ON g.subject_id = sub.id
        WHERE g.teacher_id = %s AND g.student_id = %s
        ORDER BY g.created_at DESC
        """
        return self.db.query(query, (teacher_id, student_id))

    def delete_grade(self, teacher_id, grade_id):
        """
        Deletes a grade from the database.

        :param teacher_id: The ID of the teacher.
        :param grade_id: The ID of the grade to be deleted.
        :return: The result of the database execution.
        """
        query = "DELETE FROM grades WHERE teacher_id = %s AND id = %s"
        return self.db.execute(query, (teacher_id, grade_id))

    def get_student_grade_by_student(self, student_id):
        """
        Retrieves all grades for a specific student.

        :param student_id: The ID of the student.
        :return: A list of grades.
        """
        query = """
        SELECT g.grade, g.comment, g.created_at AS date_added, sub.name
        AS subject_name, t.first_name AS teacher_name
        FROM grades g
        JOIN subjects sub ON g.subject_id = sub.id
        JOIN teachers t ON g.teacher_id = t.id
        WHERE g.student_id = %s
        ORDER BY g.created_at DESC
        """
        return self.db.query(query, (student_id,))

    def get_student_grades_by_subject(self, student_id, subject_id):
        """
        Retrieves all grades for a specific student in a specific subject.

        :param student_id: The ID of the student.
        :param subject_id: The ID of the subject.
        :return: A list of grades.
        """
        query = """
        SELECT g.grade, g.comment, g.created_at AS date_added, sub.name
        AS subject_name, t.first_name AS teacher_name
        FROM grades g
        JOIN subjects sub ON g.subject_id = sub.id
        JOIN teachers t ON g.teacher_id = t.id
        WHERE g.student_id = %s AND g.subject_id = %s
        ORDER BY g.created_at DESC
        """
        return self.db.query(query, (student_id, subject_id))
