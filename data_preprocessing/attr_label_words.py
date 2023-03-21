def attr_labels_words(documents_list, dict_json, proj_type):
    """
    Picks the list of doc and the json from label_studio and attributes a label

    Args:
        documents_list: list of doc

        dict_json: json data with bboxes of the labels

    Returns:
        does not return anything, attributes a label
    """

    for document in documents_list:
        print()
        document.attr_labels(dict_json, proj_type)

    return documents_list
