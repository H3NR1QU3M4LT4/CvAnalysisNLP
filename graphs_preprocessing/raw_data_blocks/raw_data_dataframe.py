from absl import logging
from .line_features import create_block_dataset
import pandas as pd


def create_pandas_dataframe_raw_data(dataset_lines_with_blocks):
    (
        list_id_doc,
        list_id_page,
        list_id_block,
        list_sub_labels,
        list_b_box_x1,
        list_b_box_x2,
        list_b_box_y1,
        list_b_box_y2, 
        list_width_line,
        list_height_line,     
        line_num_words,
        line_text,
    ) = create_block_dataset(dataset_lines_with_blocks)

    data = {
        "id_doc": list_id_doc,
        "id_page": list_id_page,
        "id_block": list_id_block,
        "sub_label": list_sub_labels,
        "b_box_x1":list_b_box_x1,
        "b_box_x2":list_b_box_x2,
        "_b_box_y1":list_b_box_y1,
        "b_box_y2":list_b_box_y2,
        "width_line": list_width_line,
        "height_line": list_height_line,
        "line_num_words": line_num_words,
        "line_text": line_text,
    }

    block_dataframe = pd.DataFrame(data)

    block_dataframe.to_csv("data/we_blocks_dataset/raw_data_dataframe_v1.csv", index=False)

    return block_dataframe
