def attr_labels_words(documents_list, dict_json, proj_type):
    """
    Picks the list of doc and the json from label_studio and attributes a label

    Args:
        documents_list: list of doc

        dict_json: json data with bboxes of the labels

    Returns:
        does not return anything, attributes a label
    """
    new_document_list = []
    for document in documents_list:
        if document.name in dict_json.keys():
            #document.attr_labels(dict_json, proj_type)
            document.attr_sub_labels(dict_json, proj_type)
            new_document_list.append(document)

    return new_document_list
