from app.config import Database


class ClassModel:
    """
    ClassModel handles database operations related to the 'class' table.
    """

    def __init__(self):
        """
        Initializes the ClassModel with a database connection.
        """
        self.db = Database()

    def add_class(self, name):
        """
        Adds a new class to the database.

        :param name: The name of the class to be added.
        """
        query = "INSERT INTO class (name) VALUES (%s)"
        self.db.execute(query, (name,))

    def get_all_class(self):
        """
        Retrieves all classes from the database.

        :return: A list of all classes.
        """
        sql = "SELECT * FROM class"
        return self.db.query(sql)
