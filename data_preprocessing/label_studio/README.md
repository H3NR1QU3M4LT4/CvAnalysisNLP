# Introduction 
Label Studio is an open-source data labeling tool for labeling and exploring multiple types of data. You can perform different types of labeling with many data formats, and we can also integrate Label Studio with machine learning models. 

This folder has the functions and a Class for hel us get the labeling details from the cvs.

# Start
To use this, create a virtual python environment and install label studio.
```
python3 -m venv env
source env/bin/activate
python -m pip install label-studio
```
Then activate the virtual python environment and run:
```
label-studio start
```

e.g.

![Azure Map](https://dev.azure.com/merkledach/fc14ab37-8ab8-49b8-9c53-bf7c1c004d27/_apis/git/repositories/b9246e3f-13c2-4a11-9061-d60b2ec5f241/items?path=/static/label_studio/working.png&versionDescriptor%5BversionOptions%5D=0&versionDescriptor%5BversionType%5D=0&versionDescriptor%5Bversion%5D=resume_label&resolveLfs=true&%24format=octetStream&api-version=5.0)

Then open your browser in localhost:8080

![Azure Map](https://dev.azure.com/merkledach/fc14ab37-8ab8-49b8-9c53-bf7c1c004d27/_apis/git/repositories/b9246e3f-13c2-4a11-9061-d60b2ec5f241/items?path=/static/label_studio/url.png&versionDescriptor%5BversionOptions%5D=0&versionDescriptor%5BversionType%5D=0&versionDescriptor%5Bversion%5D=resume_label&resolveLfs=true&%24format=octetStream&api-version=5.0)

It is also necessary create an account to save your projects and to get an Autentication Token



## Services
The services contains the API implementation that allow us to get projects, annotations, labels, etc.
It's require an Autentication Token wich is located in your profile page.

API Documentation: https://labelstud.io/api

e.g.
```
def get_projects():
    response = requests.get(URL + "projects/", headers=HEADERS_API).json()
    projects = []
    for element in response["results"]:
        projects.append(
            LabelStudioProject(
                element["id"], element["title"], element["created_by"]["email"]))
    return projects

def create_export(id_project):
    response = requests.post(
        URL + f"projects/{id_project}/exports/", headers=HEADERS_API).json()
    return response["id"]
```

## Label studio Project
This is a Class to help us save the projects in the label studio after an export, it contains an id_project : (int) id of the project, a title: (str) title of the project and created_by: (str)  gives the email who created the project

![Azure Map](https://dev.azure.com/merkledach/fc14ab37-8ab8-49b8-9c53-bf7c1c004d27/_apis/git/repositories/b9246e3f-13c2-4a11-9061-d60b2ec5f241/items?path=/static/label_studio/projects.png&versionDescriptor%5BversionOptions%5D=0&versionDescriptor%5BversionType%5D=0&versionDescriptor%5Bversion%5D=resume_label&resolveLfs=true&%24format=octetStream&api-version=5.0)

```
class LabelStudioProject:
    def __init__(self, id_project: int, title:str,            created_by: str):
        self.id_project = id_project
        self.title = title
        self.created_by = created_by

```