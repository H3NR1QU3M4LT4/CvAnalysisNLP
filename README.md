# CvAnalysisNLP
This project is part of my dissertation in Information Systems Engineering and aims to create models for resume parsing using LayoutLMv2, LayoutLMv3 and LayoutXML models. The project contains Jupyter notebooks for fine-tuning these models to do token classification on resume data.
The data used for fine tunning is not available.

## Requirements:

* Python 3.x
* PyTorch
* transformers library
* pandas
* numpy
* plotty
* tensorboard

NOTE: better run in google colab

## To get started with the project, follow these steps:

* Clone the repository using git clone https://github.com/your-username/resume-parsing.git
* Install the required libraries. In colab use `! pip install <package>`
* Download the pre-trained models for LayoutLMv2, LayoutLMv3 and LayoutXML from the Hugging Face model hub.
*Prepare the training data by collecting resumes from various sources and converting them into a suitable format for token classification. This can be done using tools such as OCR and PDF parsers.
* Split the data into train, validation and test sets.
* Fine-tune the models using the notebooks provided in the project.

## Folder Structure
Since not only I did token classification for sections from a CV each folder represents the main classifications:
* `Sections`: section classification like summary, work experience, education
* `WE`: work experience classification like dates, organization, description
* `EDUC`: education classification like dates, school, description, grade
* `Blocks`: divide work experince and education in blocks (text segmentation) in order to undestand better the CV structure

Also once the models are fine-tuned, the evaluation of their performance on the test set using the evaluation notebooks is provided in the project after the training.
Use the best-performing model for resume parsing. The parsed data can be stored in a suitable format such as JSON or CSV.

Note:
Since the data is not available, the notebooks have been designed to work with custom data. You need to modify the code in the notebooks to suit your data.
The notebooks assume that the data is in a certain format. If your data is in a different format, you need to modify the code accordingly.
