"""
    Module to process the input list of PDF's and save the page content in the Page class
"""

import os

from typing import List

from absl import logging
from pdf2image import convert_from_path
from PIL import Image
import pdfplumber

from .document import Document
from .page import Page
from .word import Word
from .bbox import Bbox
from .create_lines import group_word_object_by_lines_no_sub_label, create_lines, attr_page_to_lines


def pdf_processing(path_dataset_cvs: str, save_images_folder: str) -> List[Document]:
    """
    Picks words and bounding boxes and saves it in a class Page object

    Args:
        PATH_DATASET_CVS: (str) path where the cvs are located

    Returns:
        a list of Documents's
    """

    pdf_list: List[str] = sorted(os.listdir(path_dataset_cvs))
    documents: List[Document] = []

    num_doc = 1

    # for each pdf in the list we open each of its page
    # and for each element in the return fuction extract_words() we save a Word object in an array
    #
    for pdf_file in pdf_list:
        logging.info(f"Processing {pdf_file}")
        with pdfplumber.open(path_dataset_cvs + pdf_file) as pdf:
            pages: List[Page] = []
            num_page = 1
            for pdf_page in pdf.pages:
                img = pdf_page.to_image()
                size = img.original.size
                words: List[Word] = []
                id_element = 0
                for element in pdf_page.extract_words():
                    words.append(
                        Word(
                            id_element,
                            element["text"],
                            Bbox(
                                element["x0"],
                                element["top"],
                                element["x1"],
                                element["bottom"],
                                size
                            ),
                            (f"{os.path.splitext(pdf_file)[0]}-{str(num_page)}.png"),
                        )
                    )
                    id_element += 1  # increments at every element in extract_words() and represents its id

                # the id of the page has a sum 10000 with the number of the doc we are dealing with the number of page
                id_page = str(num_doc + 10000) + str(num_page)
                #img = pdf_page.to_image()

                #size = img.original.size
                path = path_dataset_cvs + pdf_file

                page = Page(int(id_page), size, words)
                pages.append(page)

                # open pdf as image
                pdf_images = convert_from_path(path)
                # idx starts at zero not one and num_page starts in 1
                idx = num_page - 1
                pdf_images[idx] = pdf_images[idx].convert("RGB")
                pdf_images[idx] = pdf_images[idx].resize(size, Image.ANTIALIAS)
                pdf_images[idx] = pdf_images[idx].save(
                    save_images_folder
                    + os.path.splitext(pdf_file)[0]
                    + "-"
                    + str(num_page)
                    + ".png"
                )

                num_page += 1  # increments at every page of the pdf_file and represents the number of the page

        documents.append(Document(num_doc, os.path.splitext(pdf_file)[0], pages))
        num_doc += 1
        logging.info(f"Created object and images from {pdf_file}")

    return documents
