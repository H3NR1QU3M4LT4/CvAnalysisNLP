"""
    Class JsonFile that has all necessary elements to retreive the list of labels of a resume
    This object is compared to the object document, because inside its content has a list of
    json_objects that are similar to the pages
"""

from typing import List
from .json_object import JsonObject


class JsonFile:
    """
    A class used to represent a JsonFile of a resume
    ...

    Attributes
    ----------
    file_name : (str) file_name

    json_objects : (List[JsonObject]) value/text of word
    """

    def __init__(self, file_name: str, json_objects: List[JsonObject]):
        self.file_name = file_name
        self.json_objects = json_objects
