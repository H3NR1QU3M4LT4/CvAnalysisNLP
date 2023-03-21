import numpy as np
from label_name_enum.label_name_enum import label_name, sub_label_name


sub_label_convert = {
    5: "NONE",
    0: "WE_JOB_TITLE",
    1: "WE_DATE",
    2: "WE_LOC",
    3: "WE_ORG",
    4: "WE_DESCRIPTION",
}


def create_sub_labels_lines(dataset_cv_labeled):
    for document in dataset_cv_labeled:
        for page in document.pages:
            if page.blocks is not None:
                for block in page.blocks:
                    for line in block.lines:
                        sub_label = []
                        for word in line.words:
                            sub_label.append(word.sub_label)

                        np_sub_label = np.array(sub_label)
                        counts = np.bincount(np_sub_label)
                        line.sub_label = np.argmax(counts)

    return dataset_cv_labeled


def get_line_section(section_name, save_lines, lines):
    temp_arr = []
    for line in lines:
        if line.label == label_name[section_name]:
            temp_arr.append(line.text)

    full_text = " ".join(temp_arr)

    save_lines.append(full_text)
    """match = find_sentences(full_text, temp_arr)
    for i in match:
        save_lines.append(i)"""


def get_we_section(page, work_experience):
    if page.blocks:
        for block in page.blocks:
            obj = {}
            if block.lines != None:
                for line in block.lines:
                    if line.sub_label in list(sub_label_name.values()):
                        if sub_label_convert[line.sub_label] in obj.keys():
                            obj[sub_label_convert[line.sub_label]] = obj.get(
                                sub_label_convert[
                                    line.sub_label]) + f' {line.text}'
                        else:
                            obj[sub_label_convert[line.sub_label]] = line.text

            work_experience.append(obj)


def create_dict_word(dataset_cv_labeled):
    dict_word = []
    for cv_file in dataset_cv_labeled:
        parsed_text = []
        summary = []
        education = []
        work_experience = []
        personal_details = []
        technical_skills = []
        languages = []
        other = []
        for page in cv_file.pages:

            """get_line_section('SUMMARY', summary, page.lines)
            get_line_section('EDUCATION', education, page.lines)
            get_line_section('PERSONAL_DETAILS', personal_details, page.lines)
            get_line_section('TECHNICAL_SKILLS', technical_skills, page.lines)
            get_line_section('LANGUAGES', languages, page.lines)
            get_line_section('OTHER', other, page.lines)"""

            get_we_section(page, work_experience)

        """parsed_text.append({'SUMMARY': {'description': summary}})
        parsed_text.append({'EDUCATION': {'description': education}})
        
        parsed_text.append(
            {'PERSONAL_DETAILS': {
                'description': personal_details
            }})
        parsed_text.append(
            {'TECHNICAL_SKILLS': {
                'description': technical_skills
            }})
        parsed_text.append({'LANGUAGES': {'description': languages}})
        parsed_text.append({'OTHER': {'description': other}})"""
        parsed_text.append({'WORK_EXPERIENCE': work_experience})

        dict_word.append({cv_file.name: parsed_text})

    return dict_word


def block_to_string(block):
    we_description = block.get('WE_DESCRIPTION')
    job_title = block.get('WE_JOB_TITLE', '')
    date = block.get('WE_DATE', '')
    loc = block.get('WE_LOC', '')
    org = block.get('WE_ORG', '')
    we_string = f'WE_JOB_TITLE: {job_title} \nWE_DATE: {date} \nWE_LOC: {loc} \nWE_ORG: {org} \nWE_DESCRIPTION: {we_description}'
    return we_string


def pair_blocks(dict_word):
    """
    Pair the blocks in the dataset and create a new dataset with the paired blocks.
    """
    block1 = []
    block2 = []
    similarity = []

    for document in dict_word:
        for filename, we_content in document.items():
            for block in we_content[0]['WORK_EXPERIENCE']:
                for block_next in we_content[0]['WORK_EXPERIENCE']:
                    we_string_next_block = block_to_string(block_next)
                    block2.append(we_string_next_block)
                    we_string = block_to_string(block)
                    block1.append(we_string)
                    similarity.append(1)
                
                for next_document in dict_word:
                    if next_document != document:
                        for filename_next, we_content_next in next_document.items():
                            for block_next_file in we_content_next[0]['WORK_EXPERIENCE']:
                                we_string_next_file_next_block = block_to_string(block_next_file)
                                block2.append(we_string_next_file_next_block)
                                we_string = block_to_string(block)
                                block1.append(we_string)
                                similarity.append(0)


    return {'block1': block1, 'block2': block2, 'similarity': similarity}