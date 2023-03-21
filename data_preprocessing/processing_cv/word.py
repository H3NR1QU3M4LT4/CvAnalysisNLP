"""
    Class Word that has all necessary elements of a word in a page from a CV
"""

import json

from label_name_enum.label_name_enum import label_name, sub_label_name
from .bbox import Bbox


class Word:
    """
    A class used to represent a Word of a page in a resume
    ...

    Attributes
    ----------
    id_word : (int) id of Word

    word : (str) value/text of word

    b_box: (List[float]) list of the bounding box arround the word

    label: (LabelName) tag of each label

    Methods
    -------
    to_json(self):
        transforms the Word object in json
        returns the value of the class in json
    """

    def __init__(
        self,
        id_word: int,
        word: str,
        b_box: Bbox,
        image_path: str,
        label=label_name["NONE"],
        sub_label=sub_label_name["NONE"],
    ):
        self.id_word = id_word
        self.word = word
        self.b_box = b_box
        self.image_path = image_path
        self.label = label
        self.sub_label = sub_label
        self.line = None
        self.block = None

    
    @property
    def text(self):
        return f'{self.word}'
    
    
    def __repr__(self) -> str:
        return str(self.text)
    
    
    # class to json
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False)
