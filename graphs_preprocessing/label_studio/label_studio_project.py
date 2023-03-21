"""
    Class LabelStudioProject that contains all the attributes of a the projects in label studio
"""


class LabelStudioProject:
    """
    A class used to represent a Label Studio Project
    ...

    Attributes
    ----------
    id_project : (int) id of the project

    title: (str) title of the project

    created_by: (str)  gives the email who created the project
    """

    def __init__(self, id_project: int, title: str, created_by: str):
        self.id_project = id_project
        self.title = title
        self.created_by = created_by
