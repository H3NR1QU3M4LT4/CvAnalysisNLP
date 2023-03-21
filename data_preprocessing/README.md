# Introduction 
This is the project that receives a bunch of resumes and returns json datasets to perform a train, validation and test

# Requirements

1.	pip install requirements
2.	Need to install ImageMagick-7.1.0-29-Q16-HDRI-x64-dll: https://download.imagemagick.org/ImageMagick/download/binaries/ImageMagick-7.1.0-34-Q16-HDRI-x64-dll.exe
3.  And gs9561w64: https://fossies.org/windows/misc/gs9561w64.exe/
3.	Activate env (Windows: .\env\Scripts\activate)

# Using
Receives four argument: the path where the CVs are stored, the path where we want to save the images, 
the path where we want to save the results, and the model we want to use

# Code
## Json Processing
```
def json_processing(json_list):
    lista = []
    for i in label_name_label_studio.keys():
        lista.append(i)

    json_list_objects = []
    for json_object in json_list:
        labels = []
        #if len(json_object['annotations']) != 0:
        for element in json_object['annotations'][0]['result']:
            if 'labels' in element['value']:
                if element['value']['labels'][0] in lista:
                    x1 = (element['value']['x'] / 100.0) * element['original_width']
                    x2 = ((element['value']['width'] / 100) * element['original_width']) + x1
                    y1 = ((element['value']['y'] / 100) *  element['original_height'])
                    y2 = ((element['value']['height'] / 100) *  element['original_height']) + y1

                    labels.append(Label(element['value']['labels'], Bbox(x1,y1,x2,y2),
                                        element['original_width'], element['original_height']))

        json_list_objects.append(JsonObject(json_object['file_upload'], labels))
   
    return json_list_objects
```

## PDF Processing
Take the list of pdf and parse them into a list os words, boundary boxes, ner tags and
the respective cv id and number of page.
```
def pdf_processing(path_dataset_cvs: str, save_images_folder: str) -> List[Document]:
    for pdf_file in pdf_list:
        with pdfplumber.open(path_dataset_cvs + pdf_file) as pdf:
            pages: List[Page] = []
            num_page = 1
            for pdf_page in pdf.pages:
                words: List[Word] = []
                id_element = 0
                for element in pdf_page.extract_words():
                    words.append(Word(id_element, element['text'], 
                                      Bbox(element['x0'],element['top'],element['x1'],element['bottom']),
                                      (os.path.splitext(pdf_file)[0] + '-' + str(num_page) + '.png')
                                      ))
                    id_element += 1 # increments at every element in extract_words() and represents its id
                
                #the id of the page has a sum 10000 with the number of the doc we are dealing with the number of page
                id_page = str(num_doc+10000) + str(num_page) 
                pages.append(Page(int(id_page), words))
                img = pdf_page.to_image()
                
                size = img.original.size
                path = path_dataset_cvs + pdf_file
                
                #open pdf as image
                pdf_images = convert_from_path(path)
                # idx starts at zero not one and num_page starts in 1
                idx = num_page - 1
                pdf_images[idx] = pdf_images[idx].convert('RGB')
                pdf_images[idx] = pdf_images[idx].resize(size, Image.ANTIALIAS)
                pdf_images[idx] = pdf_images[idx].save(save_images_folder + os.path.splitext(pdf_file)[0] + '-' + str(num_page) + '.png')
                
                num_page += 1  # increments at every page of the pdf_file and represents the number of the page
        
        #remove unwanted characters of the pdf's name
        name_doc = os.path.splitext(pdf_file)[0]
        name_doc = name_doc.replace(' ', '_')
        name_doc = name_doc.replace('(', '')
        name_doc = name_doc.replace(')', '')
        name_doc = name_doc.replace("'", '')
        name_doc = name_doc.replace(",", '')
        documents.append(Document(name_doc, pages))
        num_doc += 1
        print("\n\n\n\n\n ********************************************* \n\n\n\n\n")

    return documents
```