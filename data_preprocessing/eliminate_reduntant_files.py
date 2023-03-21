"""      
    Module to communicate with Label_studio in order to get the json export
"""
from typing import List


def eliminate_redundant_files(dataset_cv_labeled: List, path_images: str) -> List:
    """
    Alows the elimination of pages wich have more than 95% of a certain label, because this
    can affect the final usage of the dataset and can give wrongs inputs to the model

    Args:
        dataset_cv_labeled: dataset labeled
        path_images: path where the images are stored to eliminate them

    Returns:
        the dataset without the repeated images with more than 95% of a certain label
    """

    for document in dataset_cv_labeled:
        for idx, page in enumerate(document.pages):
            aux_dicti = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}

            mean = []
            count_word_experience = 0

            for word in page.words:
                path_image = word.image_path

                if word.label == 5 or word.label == 6:
                    count_word_experience += 1
                    aux_dicti[4] = count_word_experience

            aux_array = list(aux_dicti.values())
            for i in aux_array:
                mean.append(i / len(page.words))

            mean = [round(elem, 2) for elem in mean]

            for i in mean:
                if i > 0.8:
                    del document.pages[idx]
                    os.remove(path_images + path_image)
                    # remove image from folder and page from docu
    return dataset_cv_labeled
