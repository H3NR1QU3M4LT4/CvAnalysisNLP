import numpy as np

from .bbox import Bbox
from .line import Line
from .full_line import FullLine


def intersect_midles(midle_line, midle_b_box, size):
    """
    in

    Args:
        word_b_box: (Bbox) bounding box of a word

        label_b_box: (Bbox) bounding box of a label

    Returns:
        does not return anything, attributes a label to a word
    """

    width, height = size

    aux_obj = Bbox(midle_b_box.x1, midle_line.y1, midle_b_box.x2, midle_line.y2)

    percentage_between = ((midle_b_box.x1 - midle_line.x2) * 100) / width

    if percentage_between > 2.5:
        return 0
    else:
        return aux_obj.iou(midle_b_box)


def group_word_object_by_lines(words, size):
    dict_lines = {}
    counter = 0
    for idx, i in enumerate(words):
        if idx == 0:
            counter += 1
            dict_lines[counter] = [i]
        elif (
            (
                intersect_midles(
                    words[idx - 1].b_box.midle_line, i.b_box.midle_b_box, size
                )
                > 0.4
            )
            and (i.label == words[idx - 1].label)
            and (i.sub_label == words[idx - 1].sub_label)
        ):
            dict_lines[counter].append(i)
        else:
            counter += 1
            dict_lines[counter] = [i]

    return dict_lines


def group_word_object_by_lines_no_sub_label(words, size):
    dict_lines = {}
    counter = 0
    for idx, i in enumerate(words):
        if idx == 0:
            counter += 1
            dict_lines[counter] = [i]
        elif (
            (
                intersect_midles(
                    words[idx - 1].b_box.midle_line, i.b_box.midle_b_box, size
                )
                > 0.4
            )
            and (i.label == words[idx - 1].label)
        ):
            dict_lines[counter].append(i)
        else:
            counter += 1
            dict_lines[counter] = [i]

    return dict_lines


def create_lines_no_sub_label(dict_lines):
    lines = []

    for idx_line, arr_words in dict_lines.items():
        x1 = []
        x2 = []
        words_label = []
        for word in arr_words:
            x1.append(word.b_box.x1)
            x2.append(word.b_box.x2)
            y1 = word.b_box.y1
            y2 = word.b_box.y2
            words_label.append(word.label)

        b_box = Bbox(min(x1), y1, max(x2), y2)
        label_nparray = np.array(words_label)
        vals_label, counts_label = np.unique(label_nparray, return_counts=True)
        index_label = np.argmax(counts_label)
        mode_label = vals_label[index_label]

        lines.append(FullLine((idx_line - 1), b_box, arr_words, label=mode_label))

    return lines


def create_lines(dict_lines):
    lines = []

    for idx_line, arr_words in dict_lines.items():
        x1 = []
        x2 = []
        words_label = []
        words_sub_label = []
        for word in arr_words:
            x1.append(word.b_box.x1)
            x2.append(word.b_box.x2)
            y1 = word.b_box.y1
            y2 = word.b_box.y2
            words_label.append(word.label)
            words_sub_label.append(word.sub_label)
            block =  word.block

        b_box = Bbox(min(x1), y1, max(x2), y2)

        label_nparray = np.array(words_label)
        vals_label, counts_label = np.unique(label_nparray, return_counts=True)
        index_label = np.argmax(counts_label)
        mode_label = vals_label[index_label]

        sub_label_nparray = np.array(words_sub_label)
        vals_sub_label, counts_sub_label = np.unique(
            sub_label_nparray, return_counts=True
        )
        index_sub_label = np.argmax(counts_sub_label)
        mode_sub_label = vals_sub_label[index_sub_label]

        lines.append(Line((idx_line - 1), b_box, arr_words, mode_label, mode_sub_label, block))

    return lines


def attr_page_to_lines(lines, page):
    for line in lines:
        line.page = page
        for word in line.words:
            word.line = line


def assign_lines_to_documents(document_list_with_sub_labels):
    for document in document_list_with_sub_labels:
        for page in document.pages:
            dict_lines = group_word_object_by_lines(page.words, page.size)
            lines = create_lines(dict_lines)
            page.lines = lines
            attr_page_to_lines(lines, page)
            page.attr_adjacent_lines()

    return document_list_with_sub_labels


def assign_lines_to_documents_no_sub_label(document_list_with_sub_labels):
    for document in document_list_with_sub_labels:
        for page in document.pages:
            dict_lines = group_word_object_by_lines_no_sub_label(page.words, page.size)
            lines = create_lines_no_sub_label(dict_lines)
            page.full_lines = lines
            attr_page_to_lines(lines, page)
            page.attr_adjacent_full_lines()

    return document_list_with_sub_labels