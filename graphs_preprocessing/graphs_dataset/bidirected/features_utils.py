import numpy as np


def get_page_lines(page):
    all_page_lines = []
    for line in page.lines:
        all_page_lines.append(line)

    return all_page_lines


def median_values(all_page_lines):
    list_width = []
    list_height = []
    list_num_words = []
    list_x1 = []
    list_x2 = []
    list_y1 = []
    list_y2 = []
    
    for line in all_page_lines:
        list_width.append(line.b_box.x2 - line.b_box.x1)
        list_height.append(line.b_box.y2 - line.b_box.y1)
        list_num_words.append(len(line.words))
        list_x1.append(line.b_box.x1)
        list_x2.append(line.b_box.x2)
        list_y1.append(line.b_box.y1)
        list_y2.append(line.b_box.y2)
    
    list_width_np_array = np.array(list_width)
    list_height_np_array = np.array(list_height)

    median_width = np.median(list_width_np_array)
    median_height = np.median(list_height_np_array)

    return (median_width, median_height)


def mean_computation_lines(all_page_lines):
    list_width = []
    list_height = []
    for line in all_page_lines:
        list_width.append(line.b_box.x2 - line.b_box.x1)
        list_height.append(line.b_box.y2 - line.b_box.y1)

    mean_width = np.array(list_width).mean()
    mean_height = np.array(list_height).mean()

    max_width = max(list_width)
    max_height = max(list_height)

    min_width = min(list_width)
    min_height = min(list_height)

    return (mean_width, mean_height, max_width, max_height, min_width,
            min_height)
