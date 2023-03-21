"""
    Class Word that has all necessary elements of a word in a page from a CV
"""
import json

from typing import List

from sklearn.model_selection import train_test_split


class Dataset:
    """
    A class used to represent a Word of a page in a resume
    ...

    Attributes
    ----------
    id_doc : (int) id of doc with the page ex:102501

    word : (List[str]) list of words in the page

    b_box: (List[int]) list of the bounding box arround the words' page

    image_path : (str) path of the image of the page

    label: (List(int) list of tags of each words' label

    Methods
    -------
    to_json(self):
        transforms the Word object in json
        returns the value of the class in json
    """

    def __init__(
        self,
        id_doc: int,
        word: List[str],
        b_box: List[int],
        image_path: str,
        label: List[int],
    ):
        self.id_doc = id_doc
        self.word = word
        self.b_box = b_box
        self.image_path = image_path
        self.label = label


def create_json_datasets(dataset, path, path_save_json, name):
    """
    Creates the train and test datasets for a posterior load into an hugging face's dataset

    Args:
        dataset: dataset with words labeled

        path: where we want the images in the dataset to be stored for posterior training

        name: name of the final dataset not splited we want to store

    Returns:
        does not return nothing, creates 3 json datasets, a train and test, and a global dataset with train and test joined
    """

    dictionary = {"cvs": None}
    object_words_list = []

    for document in dataset:
        for page in document.pages:
            words_list = []
            b_boxes_list = []
            labels_list = []
            for word in page.words:
                words_list.append(word.word)
                b_boxes_list.append([round(x) for x in word.b_box.box])
                labels_list.append(word.label)

            object_words_list.append(
                Dataset(
                    page.id_page,
                    words_list,
                    b_boxes_list,
                    path + word.image_path,
                    labels_list,
                ).__dict__
            )
    dictionary["cvs"] = object_words_list

    json_object = json.dumps(dictionary["cvs"], default=lambda o: o.__dict__)

    # saves a json with everything
    with open(f"{path_save_json}{name}.json", "w") as outfile:
        outfile.write(json_object)

    with open(f"{path_save_json}{name}.json") as outfile:
        lines = outfile.readlines()

    # split the full dataset in 2, train and test
    json_dataset = json.loads(lines[0])
    train, val = train_test_split(json_dataset, test_size=0.30)

    val, test = train_test_split(val, test_size=0.50)

    # convert the train and test datasets in json objects
    dicti_train = {"cvs": train}
    dicti_val = {"cvs": val}
    dicti_test = {"cvs": test}
    json_object_train = json.dumps(dicti_train, default=lambda o: o.__dict__)
    json_object_val = json.dumps(dicti_val, default=lambda o: o.__dict__)
    json_object_test = json.dumps(dicti_test, default=lambda o: o.__dict__)

    # save the train and test datasets as json files
    with open(f"{path_save_json}train.json", "w") as outfile:
        outfile.write(json_object_train)

    with open(f"{path_save_json}validation.json", "w") as outfile:
        outfile.write(json_object_val)

    with open(f"{path_save_json}test.json", "w") as outfile:
        outfile.write(json_object_test)
