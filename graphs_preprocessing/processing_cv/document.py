"""
    Class Document that has all necessary elements of PDF/CV
"""

import json
from typing import List

from .page import Page


class Document:
    """
    A class used to represent a PDF document
    ...

    Attributes
    ----------
    name : (name) name of pdf file

    pages: (List[Page]) list of pages that are in the CV

    Methods
    -------
    to_json(self):
        transforms the document object in json
        returns the value of the class in json

    attr_labels(self, json_dic):
        if in the json_dict there is a doc with the same name as the doc
        then attribute a label to each word in the respective page
    """

    def __init__(self, id_doc: int, name: str, pages: List[Page]):
        self.id_doc = id_doc
        self.name = name
        self.pages = pages

    # class to json
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False)

    def attr_labels(self, json_dic, proj_type):
        # if there is a json object with the same name as the document
        if json_dic[self.name]:
            # for each page assign a specific label
            for idx, page in enumerate(self.pages):
                page.attr_labels(json_dic[self.name], proj_type)

    def attr_sub_labels(self, json_dic, proj_type):
        # if there is a json object with the same name as the document
        if json_dic[self.name]:
            # for each page assign a specific label
            for idx, page in enumerate(self.pages):
                page.attr_sub_labels(json_dic[self.name], proj_type)
