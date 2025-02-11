from app.config import Database


class SubjectModel:
    """
    SubjectModel handles database operations related to the 'subjects' table.
    """

    def __init__(self):
        """
        Initializes the SubjectModel with a database connection.
        """
        self.db = Database()

    def add_subject(self, name):
        """
        Adds a new subject to the database.

        :param name: The name of the subject to be added.
        """
        query = "INSERT INTO subject (name) VALUES (%s)"
        self.db.execute(query, (name,))

    def get_all_subjects(self):
        """
        Retrieves all subjects from the database.

        :return: A list of all subjects.
        """
        sql = "SELECT * FROM subjects"
        return self.db.query(sql)

    def get_languages(self):
        """
        Retrieves all language subjects from the database.

        :return: A list of language subjects.
        """
        sql = """SELECT id, name FROM subjects WHERE type = 'language'
        ORDER BY name ASC"""
        return self.db.query(sql)

    def get_options(self):
        """
        Retrieves all optional subjects from the database.

        :return: A list of optional subjects.
        """
        sql = """SELECT id, name FROM subjects WHERE type = 'option'
        ORDER BY name ASC"""
        return self.db.query(sql)
