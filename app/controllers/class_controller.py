from app.models.class_ import ClassModel


class ClassController:
    """
    ClassController handles the logic for class-related operations.
    """

    def __init__(self):
        """
        Initializes the ClassController with the necessary model.
        """
        self.class_model = ClassModel()

    def get_all_classes(self):
        """
        Retrieves all classes.

        :return: A list of all classes.
        """
        return self.class_model.get_all_class()

    def add_class(self, name):
        """
        Adds a new class.

        :param name: The name of the class to be added.
        :return: A success message.
        """
        self.class_model.add_class(name)
        return {"success": "Class added successfully"}
