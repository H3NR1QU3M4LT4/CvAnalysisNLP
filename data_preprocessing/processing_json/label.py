"""
    Class Label that has all necessary elements a label: name and bounding boxes
"""

from processing_cv.bbox import Bbox


class Label:
    """
    A class used to represent a Label in a resume
    ...

    Attributes
    ----------
    id_label : (int) id of Word

    name : (LabelName) value/text of word

    b_box: (List[float]) list of the bounding box arround the label
    """

    def __init__(self, name: str, b_box: Bbox, original_width: int, original_height: int):
        self.name = name
        self.b_box = b_box
        self.original_width = original_width
        self.original_height = original_height
