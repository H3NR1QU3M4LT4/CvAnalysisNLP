def create_block_dataset(dataset_lines_with_blocks):
    list_id_doc = []
    list_id_page = []
    list_id_block = []
    list_sub_labels = []
    list_b_box_x1 = []
    list_b_box_x2 = []
    list_b_box_y1 = []
    list_b_box_y2 = []
    list_width_line = []
    list_height_line = []
    line_num_words = []
    line_text = []
    
    for document in dataset_lines_with_blocks:
        for page in document.pages:
            if page.blocks:
                for block in page.blocks:
                    for line in block.lines:
                        list_id_doc.append(document.id_doc)
                        list_id_page.append((page.page_number + 1))
                        list_id_block.append(block.id_block)
                        list_sub_labels.append(line.sub_label)
                        list_b_box_x1.append(line.b_box.x1)
                        list_b_box_x2.append(line.b_box.x2)
                        list_b_box_y1.append(line.b_box.y1)
                        list_b_box_y2.append(line.b_box.y2)

                        width = line.b_box.x2 - line.b_box.x1
                        list_width_line.append(width)
                    
                        height = line.b_box.y2 - line.b_box.y1
                        list_height_line.append(height)

                        line_num_words.append(len(line.words))
                        line_text.append(line.text)

    return (    list_id_doc,
    list_id_page,
    list_id_block,
    list_sub_labels,
    list_b_box_x1,
    list_b_box_x2,
    list_b_box_y1,
    list_b_box_y2,
    list_width_line,
    list_height_line,
    line_num_words,
    line_text,)
