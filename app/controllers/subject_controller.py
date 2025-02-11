from app.models.subject import SubjectModel


class SubjectController:
    """
    SubjectController handles the logic for subject-related operations.
    """

    def __init__(self):
        """
        Initializes the SubjectController with the necessary model.
        """
        self.model = SubjectModel()

    def get_all_subjects(self):
        """
        Retrieves all subjects.

        :return: A list of all subjects.
        """
        return self.model.get_all_subjects()

    def get_languages(self):
        """
        Retrieves all language subjects.

        :return: A list of language subjects.
        """
        return self.model.get_languages()

    def get_options(self):
        """
        Retrieves all optional subjects.

        :return: A list of optional subjects.
        """
        return self.model.get_options()
