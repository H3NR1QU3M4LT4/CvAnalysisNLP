import pickle
from absl import app, flags
from dataset import create_json_datasets
from processing_cv.pdf_processing import pdf_processing
from processing_cv.create_lines import assign_lines_to_documents_no_sub_label
from attr_label_words import attr_labels_words
from processing_json.json_processing import json_processing, pair_same_json_objects
from label_studio.services import (
    get_projects,
    create_export,
    download_export,
    get_id_required_project,
)
from eliminate_reduntant_files import eliminate_redundant_files
from data_analysis.pandas import create_pandas_for_analysis
from data_analysis.document_analysis import create_features_for_analysis


FLAGS = flags.FLAGS

#--PATH_DATASET_CVS=
#--SAVE_IMAGES_FOLDER=C:/Users/steixe01/Documents/folder_data_resume_parser/dataset_cvs_images/
flags.DEFINE_string("PATH_DATASET_CVS", None, "Folder where the resumes are stored")

flags.DEFINE_string(
    "SAVE_IMAGES_FOLDER",
    None,
    "Folder where the converted pdf to image should be stored",
)

flags.DEFINE_string("SAVE_JSON", None, "Folder where test json should be stored")


def main(_):
    
    # create a list of Document's with name, page, labels, words and save images
    dataset_cv = pdf_processing(FLAGS.PATH_DATASET_CVS, FLAGS.SAVE_IMAGES_FOLDER)

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
    dataset_cv_labeled = attr_labels_words(dataset_cv, json_file_list_objects, "with_IB")

    document_list_with_full_lines = assign_lines_to_documents_no_sub_label(
            dataset_cv_labeled)

    # in case you want reduced error images with full pges of work experience uncomment the next line
    # however after testing a full dataset provides better performance
    # dataset_cv_labeled = eliminate_redundant_files(dataset_cv_labeled, FLAGS.SAVE_IMAGES_FOLDER)

    # create the train and val datasets
    create_json_datasets(
        dataset_cv_labeled, '/content/drive/MyDrive/cv_images/', FLAGS.SAVE_JSON, "full_json"
    )
    
    with open('document_list_with_lines.pickle','wb') as f:
            pickle.dump(document_list_with_full_lines, f)
    """
    with open('document_list_with_lines.pickle','rb') as f:
            document_list_with_full_lines = pickle.load(f)

    dataframe = create_pandas_for_analysis(document_list_with_full_lines)
    document_list_with_full_lines = create_features_for_analysis(document_list_with_full_lines)"""

if __name__ == "__main__":
    app.run(main)
