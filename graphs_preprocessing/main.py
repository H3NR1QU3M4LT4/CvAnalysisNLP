"""
    Main module where we have all the logical actions
    To run this first we need to active the virtual env: .\env\Scripts\ activate

    The main function gets the arg file that sould be the path folder containing cvs in pdf
    Then we parse the pdf and save the words, bounding boxes, etc
"""
import pickle
import os
from absl import app, flags
import pandas as pd
from dataset import create_json_datasets
from processing_cv.pdf_processing import pdf_processing
from processing_cv.create_lines import assign_lines_to_documents_no_sub_label, assign_lines_to_documents
from we_blocks.attr_blocks import add_blocks_to_documents
from attr_label_words import attr_labels_words
from graphs_dataset.bidirected.create_tensors import create_tensors_from_all_nodes_connected
from graphs_dataset.directed.create_tensors import create_tensors_from_lines_data
from json_processing import json_processing, pair_same_json_objects
from we_blocks.block_dataframe import create_pandas_dataframe_without_embedding
from raw_data_blocks.raw_data_dataframe import create_pandas_dataframe_raw_data
from label_studio.services import (
    get_projects,
    create_export,
    download_export,
    get_id_required_project,
)
from pair_blocks import create_dict_word, create_sub_labels_lines, pair_blocks


FLAGS = flags.FLAGS

flags.DEFINE_string("PATH_DATASET_CVS", None,
                    "Folder where the resumes are stored")

flags.DEFINE_string(
    "SAVE_IMAGES_FOLDER",
    None,
    "Folder where the converted pdf to image should be stored",
)

flags.DEFINE_string("SAVE_JSON", 'data/we_sub_labels_dataset/',
                    "Folder where test json should be stored")


def main(_):
    if not os.path.exists(
            'data/picke_objects/array_object_dataset_lines_with_blocks.pickle'
    ) and not os.path.exists(
            'data/picke_objects/document_list_with_lines.pickle'):
        
        # create a list of Document's with name, page, labels, words and save images
        dataset_cv = pdf_processing(FLAGS.PATH_DATASET_CVS,
                                    FLAGS.SAVE_IMAGES_FOLDER)

        # get allprojects, display them and we choose one to export
        label_studio_projects = get_projects()
        id_project = get_id_required_project(label_studio_projects)
        id_export = create_export(id_project)
        json_list = download_export(id_project, id_export)

        # pick the json reponse and we save only the things we want such as name, labels
        json_list_objects = json_processing(json_list)

        # pair the same pages into the same json_file
        json_file_list_objects = pair_same_json_objects(json_list_objects)

        # attribute labels to each word
        dataset_cv_labeled = attr_labels_words(dataset_cv,
                                               json_file_list_objects,
                                               "with_IB")
            
        document_list_with_full_lines = assign_lines_to_documents_no_sub_label(
            dataset_cv_labeled)

        document_list_with_lines = assign_lines_to_documents(
            document_list_with_full_lines)

        dataset_lines_with_blocks = add_blocks_to_documents(
            document_list_with_lines, json_file_list_objects)

        with open(
                'data/picke_objects/array_object_dataset_lines_with_blocks.pickle',
                'wb') as f:
            pickle.dump(dataset_lines_with_blocks, f)

        with open('data/picke_objects/document_list_with_lines.pickle',
                  'wb') as f:
            pickle.dump(document_list_with_lines, f)
    
    else:
        # Open the file in binary mode
        with open(
                'data/picke_objects/array_object_dataset_lines_with_blocks.pickle',
                'rb') as f:
            # Call load method to deserialze
            dataset_lines_with_blocks = pickle.load(f)

        with open('data/picke_objects/document_list_with_lines.pickle',
                  'rb') as f:
            document_list_with_lines = pickle.load(f)

    # create the train and val datasets
    
    create_json_datasets(
        dataset_lines_with_blocks,
        '/content/drive/MyDrive/sublabels_cv_images/', #FLAGS.SAVE_IMAGES_FOLDER,
        FLAGS.SAVE_JSON,
        "json_dataset_sublabels",
    )
    """
    dataframe = pd.read_csv('C:/Users/steixe01/source/repos/ResumeParser/data_creation/dataframe_analysis.csv')
    
    
    document_list_with_lines = create_sub_labels_lines(document_list_with_lines)

    dicti = create_dict_word(document_list_with_lines)

    ola = pair_blocks(dicti)

    block_dataframe = pd.DataFrame(ola)
    block_dataframe = block_dataframe.drop_duplicates()
    block_dataframe = block_dataframe.reset_index(drop=True)
    block_dataframe.to_csv("data/positions.csv", index=False)"""
    """
    raw_data = create_pandas_dataframe_raw_data(dataset_lines_with_blocks)
    block_dataset = create_pandas_dataframe_without_embedding(
        dataset_lines_with_blocks)

    block_dataset_emdding = create_pandas_dataframe_with_embedding(block_dataset)
    
    data = create_tensors_from_all_nodes_connected(dataset_lines_with_blocks,
        'data/graph_tensor/')
    

    with open('data/graph_tensor/data_bidirected_median_embedding.pickle',
              'wb') as f:
            pickle.dump(data, f)
    """
            

if __name__ == "__main__":
    app.run(main)
