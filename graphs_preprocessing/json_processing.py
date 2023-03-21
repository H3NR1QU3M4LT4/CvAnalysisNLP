"""
    Module to process the input list of json and save the boundray boxes content 
"""
import uuid
from typing import List

from we_blocks.we_block import We_Block
from processing_json.json_object import JsonObject
from processing_json.json_file import JsonFile
from processing_json.label import Label
from label_name_enum.label_name_enum import label_name_label_studio, label_name
from processing_cv.bbox import Bbox


def json_processing(json_list):
    """
    The json that is exported from label studio has a lot of elements and we get only the
    necessaries:  bounding boxes, labels and file name and passes it throw the respective objects

    Args:
        path_json: (str) path where the jsons are located

    Returns:
        a list of json_files parsed in only the parameters we want
    """

    json_list_objects = []
    for json_object in json_list:
        labels = []
        blocks = []
        counter = 0
        if len(json_object["annotations"]) != 0:
            for element in json_object["annotations"][0]["result"]:
                if "labels" in element["value"]:
                    if element["value"]["labels"][0] in list(
                        label_name_label_studio.keys()
                    ):
                        x1 = (element["value"]["x"] / 100.0) * element["original_width"]
                        x2 = (
                            (element["value"]["width"] / 100)
                            * element["original_width"]
                        ) + x1
                        y1 = (element["value"]["y"] / 100) * element["original_height"]
                        y2 = (
                            (element["value"]["height"] / 100)
                            * element["original_height"]
                        ) + y1

                        labels.append(
                            Label(
                                str(element["value"]["labels"][0]),
                                Bbox(x1, y1, x2, y2),
                                element["original_width"],
                                element["original_height"],
                            )
                        )

                        if element["value"]["labels"][0] in list(label_name.keys()):
                            x1_block = (element["value"]["x"] / 100.0) * element[
                                "original_width"
                            ]
                            x2_block = (
                                (element["value"]["width"] / 100)
                                * element["original_width"]
                            ) + x1_block
                            y1_block = (element["value"]["y"] / 100) * element[
                                "original_height"
                            ]
                            y2_block = (
                                (element["value"]["height"] / 100)
                                * element["original_height"]
                            ) + y1_block

                            counter += 1
                            blocks.append(
                                We_Block(
                                    int(counter),
                                    Bbox(x1_block, y1_block, x2_block, y2_block),
                                    str(element["value"]["labels"][0]),
                                )
                            )

            json_list_objects.append(JsonObject(json_object["file_upload"], labels, blocks))

        else:
            json_list_objects.append(JsonObject(json_object["file_upload"], labels))

    return json_list_objects


def pair_same_json_objects(json_list_objects) -> List[JsonFile]:
    """
    Pair the same belonging json objects

    Args:
        json_list_objects: list of the json data from label_studio

    Returns:
        a list of json objects paired in the same file
    """

    dict_json_objects = {}
    for json_object in json_list_objects:
        if json_object.formated_file_name in dict_json_objects.keys():
            dict_json_objects[json_object.formated_file_name].append(json_object)
        else:
            dict_json_objects[json_object.formated_file_name] = [json_object]

    # sort the files to have the right pages in the right place
    for value_dict in dict_json_objects.values():
        value_dict = value_dict.sort(key=lambda json_object: json_object.page_number)

    return dict_json_objects
