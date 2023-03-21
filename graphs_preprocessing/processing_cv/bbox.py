"""
    Module is used to define a bounding box
"""


class Bbox:
    """
    A class used to represent a bounding box
    ...

    Attributes
    ----------
    x1: (float) Distance of left side of character from left side of page

    y1: (float) Distance of right side of character from left side of page

    x2: (float) Distance of top of character from top of page

    y2: (float) Distance of bottom of the character from top of page

    box: array of the bounding boxes [x1,y1,x2,y2]

    Methods
    -------
    area (self):
        Calculates the surface area.
        returns the value of the area

    intersect (self, bbox):
        Calculates the area of the intersection between two Bboxs
        returns its value

    iou (self, bbox):
        Calculates the percentage of intersetion
        returns the intersection over union value between 0 and 1
    """

    def __init__(self, x1, y1, x2, y2, size=None):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)
        self.box = [self.x1, self.y1, self.x2, self.y2]
        self.size = size

    @property
    def area(self):
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1)

    @property
    def midle_line(self):
        middle = int((self.y2 - self.y1) / 2)
        return Bbox(self.x1, middle + self.y1, self.x2, middle + self.y1)

    @property
    def midle_b_box(self):
        middle = int((self.y2 - self.y1) / 2)
        return Bbox(self.x1, middle + self.y1 - 2, self.x2, middle + self.y1 + 2)

    def intersect(self, bbox):
        x1 = max(self.x1, bbox.x1)
        y1 = max(self.y1, bbox.y1)
        x2 = min(self.x2, bbox.x2)
        y2 = min(self.y2, bbox.y2)
        intersection = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
        return intersection

    def iou(self, bbox):
        intersection = self.intersect(bbox)

        iou = intersection / float(self.area)

        return iou
