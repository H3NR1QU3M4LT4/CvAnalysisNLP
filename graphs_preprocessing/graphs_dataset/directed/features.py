import numpy as np
from absl import logging
from sklearn.preprocessing import OneHotEncoder

from .features_utils import get_page_lines, mean_computation_lines, median_values
from label_name_enum.label_name_enum import sub_label_name, label_name

from sentence_transformers import SentenceTransformer


dictarr = np.asarray(list(sub_label_name.values())).reshape(-1, 1)
enc = OneHotEncoder(sparse=False)
enc.fit(dictarr)


def sentence_embedding(line_text):
    logging.info("Encondig:", line_text)
    encoder_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    line_enconding = encoder_model.encode(line_text)
    return line_enconding.tolist()


def get_line_features(line, mean_width, mean_height, max_width, max_height,
                      min_width, min_height, median_width, median_height,
                      size):
    
    w, h = size
    
    # WIDTH
    width_line = line.b_box.x2 - line.b_box.x1
    normalized_width_line = width_line / mean_width
    normalized_width_median_line = width_line / median_width
    norm_width_h = width_line / median_height

    # HEIGTH
    height_line = line.b_box.y2 - line.b_box.y1
    normalized_height_line = height_line / mean_height
    normalized_height_median_line = height_line / median_height

    #Normalize width with max and min
    mm_normalized_width_line = (((width_line - min_width) /
                                 (max_width - min_width))
                                if max_width != min_width else
                                ((width_line - min_width) / 1))

    # HEIGTH
    mm_normalized_height_line = (((height_line - min_height) /
                                  (max_height - min_height))
                                 if max_height != min_height else
                                 ((height_line - min_height) / 1))
    
    norm_num_words = 1 / len(line.words)
    norm_x1 = line.b_box.x1 / w
    norm_x2 = line.b_box.x2 / w
    norm_y1 = line.b_box.y1 / h
    norm_y2 = line.b_box.y2 / h
    
    line_enconding = sentence_embedding(line.text)

    return [
        norm_width_h, normalized_height_median_line,
        mm_normalized_width_line, mm_normalized_height_line,
        norm_num_words, norm_x1, norm_x2, norm_y1,
        norm_y2
    ]  + line_enconding


def graph_features(document, document_page):
    all_lines_features = []
    
    for page in document.pages:
        all_page_lines = get_page_lines(page)
        (mean_width, mean_height, max_width, max_height, min_width,
         min_height) = mean_computation_lines(all_page_lines)
        (median_width, median_height) = median_values(all_page_lines)
         
    for line in document_page.full_lines:
        if line.label == label_name["WORK_EXPERIENCE"]:
            line_features = get_line_features(line, mean_width, mean_height,
                                              max_width, max_height, min_width,
                                              min_height, median_width, median_height, document_page.size)
            all_lines_features.append(line_features)
    
    return all_lines_features