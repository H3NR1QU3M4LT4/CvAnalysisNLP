"""
    Class JsonObject that has all necessary elements to retreive the list of labels of a resume
    This object is compared as a page from a resume the only diference is this object has a list of
    the exisiting labels in the resume's page and its bounding boxes
"""

import os
from typing import List

from .label import Label


class JsonObject:

    """
    A class used to represent a JsonObject of a resume
    ...

    Attributes
    ----------
    file_name : (int) name of the file

    labels : (List[Label]) list of labels with its bbox and name

    Methods
    -------
    formated_file_name(self):
        returns the name of the document without the ids from label studio

    page_number(self):
        returns the number of the page
    """

    def __init__(self, file_name: str, labels: List[Label], blocks=None):
        self.file_name = file_name
        self.labels = labels
        self.blocks = blocks

    @property
    def formated_file_name(self):
        name = self.file_name[9:]
        name = os.path.splitext(name)[0]

        # we split to get the number of the page
        number = name.split("-")[-1]

        # if the number has 1 element means that the page its between 1 and 9
        # else more than 9 and less than 99
        # and we return only the name without the numbers of the page and the '-'

        if len(number) == 1:
            name = name[:-2]
        else:
            name = name[:-3]

        return name

    @property
    def page_number(self):
        name = os.path.splitext(self.file_name)[0]
        number = int(name.split("-")[-1])
        return number
