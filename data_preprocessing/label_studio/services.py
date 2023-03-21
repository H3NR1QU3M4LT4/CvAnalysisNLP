# we use Label Studio: https://github.com/heartexlabs/label-studio

"""      
    Module to communicate with Label_studio in order to get the json export
"""

import requests

from absl import logging

# Authorization token
from config import API_LABEL_STUDIO

from .label_studio_project import LabelStudioProject

URL = "http://localhost:8080/api/"

HEADERS_API = {"Authorization": f"TOKEN {API_LABEL_STUDIO}"}

# VALIDATION TOKEN


def get_users():
    """
    get the users in Label Studio

    Returns:
        a list of json objects with the information of the users in the plataform
    """

    response = requests.get(URL + "users/", headers=HEADERS_API).json()
    return response


def get_projects():
    """
    get the existing projects in Label Studio

    Returns:
        a list of LabelStudioProject objects
    """

    response = requests.get(URL + "projects/", headers=HEADERS_API).json()
    projects = []
    for element in response["results"]:
        projects.append(
            LabelStudioProject(
                element["id"], element["title"], element["created_by"]["email"]
            )
        )
    return projects


def create_export(id_project):
    """
    Creates an export action to export the content of the project

    Args:
        id_project: (int) id of the project we want to export

    Returns:
        the id of the export action
    """

    response = requests.post(
        URL + f"projects/{id_project}/exports/", headers=HEADERS_API
    ).json()
    return response["id"]


def get_created_exports(id_project, id_export):
    """
    Gets a certain export action of a certain project

    Args:
        id_project: (int) id of the project we want to export

        id_export: (int) id of the export action created

    Returns:
        the response with who created, when and status
    """

    response = requests.get(
        URL + f"projects/{id_project}/exports/{id_export}", headers=HEADERS_API
    ).json()
    return response


def download_export(id_project, id_export):
    """
    "Downloads" the export action of the project containing the labels we want

    Args:
        id_project: (int) id of the project we want to export

        id_export: (int) id of the export ac
        tion created

    Returns:
        a list of json objects with the information of the users in the plataform
    """

    response = requests.get(
        URL + f"projects/{id_project}/exports/{id_export}/download", headers=HEADERS_API
    ).json()
    return response


def get_id_required_project(label_studio_projects):
    """
    Asks the user the prpject in label studio that we want deal with

    Args:
        label_studio_projects: (List) ids of the existing projects in label studio

    Returns:
        the id of the required project
    """

    for project in label_studio_projects:
        logging.info(f"ID: {project.id_project} --- TITLE: {project.title}")
    logging.info("Insert the required ID project:")
    id_project = input()
    return id_project
