import json
from typing import List

import numpy as np

from .word import Word
from .bbox import Bbox


class FullLine:
    """
    A class used to represent a line of text in a page of a pdf
    ...

    Attributes
    ----------
    id_line : (int) start in 0

    text: (str) joined words

    words: (List[Word]) list of words that are in the line

    Methods
    -------
    to_json(self):
        transforms the Page object in json
        returns the value of the class in json
    """

    def __init__(
        self, id_line: int, b_box: Bbox, words: List[Word], label=None
    ):
        self.id_line = id_line
        self.b_box = b_box
        self.words = words
        self.label = label
        self.block = None
        self.page = None
        self.lines_up = None
        self.lines_down = None
        self.lines_left = None
        self.lines_right = None

    # convert class to json
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False)

    @property
    def text(self):
        text = []
        for word in self.words:
            text.append(word.word)

        return " ".join(text)

    def __repr__(self) -> str:
        return str(self.text)
