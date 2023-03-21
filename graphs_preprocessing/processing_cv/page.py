"""
    Class Page that has all necessary elements of a pdf page from a CV
"""

import json
from typing import List
from label_name_enum.label_name_enum import label_name, sub_label_name, label_name_IB, sub_label_name_IB

from .word import Word
from .line import Line
from .full_line import FullLine
from .create_lines import intersect_midles


class Page:
    """
    A class used to represent a Page of a PDF
    ...

    Attributes
    ----------
    id_page : (int) id of page ex: 100011 ('10000 + id_doc' + 'num_page')

    size: (tuple[int, int]) width and height of a image

    words: (List[Word]) list of words that are in the page of CV

    lines: (List[Lines]) list of lines that are in the page of CV

    Methods
    -------
    to_json(self):
        transforms the Page object in json
        returns the value of the class in json

    attr_labels(self, json_dic):
        attribute a label to each word in the respective page
    """

    def __init__(
        self,
        id_page: int,
        size,
        words: List[Word],
        lines: List[Line] = None,
        blocks: List[object] = None,  # remove this parameter
        full_lines: List[FullLine] = None,
    ):
        self.id_page = id_page
        self.size = size
        self.words = words
        self.lines = lines
        self.blocks = blocks
        self.full_lines = full_lines

    @property
    def page_number(self):
        a = self.id_page
        # transform id into an array
        num_page = [int(x) for x in str(a)]
        b = num_page
        # beacuse the id begins always with 10000 if the document as more than 9 pages
        # then we will have an array b with more than 6 positions ex: 1035010 (id_doc=350, num_page=10)

        if len(b) == 6:
            b = b[-1:][0] - 1  # index for get the right page in json_data
        else:
            fst_alg = str(b[-2:][0])
            snd_alg = str(b[-2:][1])
            b = int(fst_alg + snd_alg) - 1

        return b

    # convert class to json
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False)

    def attr_labels(self, json_data, proj_type):
        a = self.id_page
        # transform id into an array
        num_page = [int(x) for x in str(a)]
        b = num_page
        # beacuse the id begins always with 10000 if the document as more than 9 pages
        # then we will have an array b with more than 6 positions ex: 1035010 (id_doc=350, num_page=10)

        if len(b) == 6:
            b = b[-1:][0] - 1  # index for get the right page in json_data
        else:
            fst_alg = str(b[-2:][0])
            snd_alg = str(b[-2:][1])
            b = int(fst_alg + snd_alg) - 1

        previous_aux_x = None
        # for each word in the doc we try to assign a label of the json
        for word in self.words:
            # same json object of the page we are dealign with
            json_page = json_data[b]
            # for each label of the json_object we determin its intersection
            for label in json_page.labels:
                if label.name in list(label_name.keys()):
                    # if there is intersection then the word label is updated
                    # ex: words: Work Experience intersection with Work Experience > 0.4
                    # Work Experience != None then label of work is B-Work Experience and previous_aux_x is Work Experience
                    # Work Experience == Work Experience then label of experience is I-Work Experience
                    if proj_type == "without_IB":
                        if intersect_rectangle(word.b_box, label.b_box) > 0.4:
                            word.label = label_name[f"{label.name}"]

                    if proj_type == "with_IB":
                        if intersect_rectangle(word.b_box, label.b_box) > 0.4:
                            if label.name[0] == previous_aux_x:
                                word.label = label_name_IB[f"I-{label.name}"]
                            else:
                                word.label = label_name_IB[f"B-{label.name}"]

                                previous_aux_x = label.name[0]

    def attr_sub_labels(self, json_data, proj_type):
        print(sub_label_name_IB)
        a = self.id_page
        # transform id into an array
        num_page = [int(x) for x in str(a)]
        b = num_page
        # beacuse the id begins always with 10000 if the document as more than 9 pages
        # then we will have an array b with more than 6 positions ex: 1035010 (id_doc=350, num_page=10)

        if len(b) == 6:
            b = b[-1:][0] - 1  # index for get the right page in json_data
        else:
            fst_alg = str(b[-2:][0])
            snd_alg = str(b[-2:][1])
            b = int(fst_alg + snd_alg) - 1

        previous_aux_x = None
        # for each word in the doc we try to assign a label of the json
        for word in self.words:
            # same json object of the page we are dealign with
            json_page = json_data[b]
            # for each label of the json_object we determin its intersection
            for label in json_page.labels:
                if label.name in list(sub_label_name.keys()):
                    # if there is intersection then the word label is updated
                    # ex: words: Work Experience intersection with Work Experience > 0.4
                    # Work Experience != None then label of work is B-Work Experience and previous_aux_x is Work Experience
                    # Work Experience == Work Experience then label of experience is I-Work Experience
                    if proj_type == "without_IB":
                        if intersect_rectangle(word.b_box, label.b_box) > 0.4:
                            word.sub_label = sub_label_name[f"{label.name}"]

                    if proj_type == "with_IB":
                        if intersect_rectangle(word.b_box, label.b_box) > 0.4:
                            print(sub_label_name_IB[f"I-{label.name}"])
                            print(sub_label_name_IB[f"B-{label.name}"])
                            if label.name[0] == "NONE":
                                word.sub_label = sub_label_name_IB[f"{label.name}"]
                            if label.name[0] == previous_aux_x:
                                word.sub_label = sub_label_name_IB[f"I-{label.name}"]
                            else:
                                word.sub_label = sub_label_name_IB[f"B-{label.name}"]

                                previous_aux_x = label.name[0]

    def attr_adjacent_lines(self):
        for idx, line in enumerate(
            self.lines[:-1]
        ):  # last item doesn't have a next line to work with
            if condition_line_right_or_left(line, self.lines[idx + 1], self.size):
                line.lines_right = [self.lines[idx + 1]]
                self.lines[idx + 1].lines_left = [line]

            stop = idx + 1
            for other_line in self.lines[stop:]:
                if line.lines_down:  # se já existir uma linha abaixo da linha line
                    if condition_line_right_or_left(
                        other_line, line.lines_down[0], self.size
                    ) and condition_line_up_or_down(line, other_line):
                        line.lines_down.append(other_line)
                        if other_line.lines_up:
                            other_line.lines_up.append(line)
                        else:
                            other_line.lines_up = [line]
                    else:
                        break

                elif condition_line_up_or_down(line, other_line):
                    line.lines_down = [other_line]
                    if other_line.lines_up:
                        other_line.lines_up.append(line)
                    else:
                        other_line.lines_up = [line]
    
    
    def attr_adjacent_full_lines(self):
        for idx, line in enumerate(
            self.full_lines[:-1]
        ):  # last item doesn't have a next line to work with
            if condition_line_right_or_left(line, self.full_lines[idx + 1], self.size):
                line.lines_right = [self.full_lines[idx + 1]]
                self.full_lines[idx + 1].lines_left = [line]

            stop = idx + 1
            for other_line in self.full_lines[stop:]:
                if line.lines_down:  # se já existir uma linha abaixo da linha line
                    if condition_line_right_or_left(
                        other_line, line.lines_down[0], self.size
                    ) and condition_line_up_or_down(line, other_line):
                        line.lines_down.append(other_line)
                        if other_line.lines_up:
                            other_line.lines_up.append(line)
                        else:
                            other_line.lines_up = [line]
                    else:
                        break

                elif condition_line_up_or_down(line, other_line):
                    line.lines_down = [other_line]
                    if other_line.lines_up:
                        other_line.lines_up.append(line)
                    else:
                        other_line.lines_up = [line]


def intersect_rectangle(word_b_box, label_b_box):
    """
    return a value between 0 and 1 corresponding to the intersection
    area between a word bbox and a bbox from a label


    Args:
        word_b_box: (Bbox) bounding box of a word

        label_b_box: (Bbox) bounding box of a label

    Returns:
        a value between 0 and 1
    """

    return word_b_box.iou(label_b_box)


def condition_line_right_or_left(line_x, line_y, size):
    """
    check if the line_x is right or left of the line_y

    Args:
    line_x: (Line) line x

    line_y: (Line) line y

    Returns:
        bool: True or False
              (True if the line_x is right or left of the line_y)
    """
    return (
        intersect_midles(
            line_x.b_box.midle_line,
            line_y.b_box.midle_b_box,
            size,
        )
        > 0.5
    )


def condition_line_up_or_down(line_x, line_y):
    """
    check if the line_x is up or down of the line_y

    Args:
    line_x: (Line) line x

    line_y: (Line) line y

    Returns:
        bool: True or False
              (True if the line_x is up or down of the line_y)
    """
    return (line_y.b_box.x1 <= line_x.b_box.x2) and (line_y.b_box.x2 >= line_x.b_box.x1)
