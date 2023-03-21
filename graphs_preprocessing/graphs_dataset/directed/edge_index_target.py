from label_name_enum.label_name_enum import label_name


def get_adjacent_lines(position_lines, line, convert_line_id_to_id_node, nodes,
                       edges):
    if line.block and position_lines:
        for positioned_line in position_lines:
            if positioned_line.label == label_name["WORK_EXPERIENCE"]:
                if positioned_line.block:
                    if line.block.id_block == positioned_line.block.id_block:
                        nodes.append(convert_line_id_to_id_node[line.id_line])
                        edges.append(convert_line_id_to_id_node[
                            positioned_line.id_line])


def edge_index_target(document_page):
    nodes = []
    edges = []
    convert_line_id_to_id_node = {}
    for idx, line in enumerate([
            line for line in document_page.full_lines
            if line.label == label_name["WORK_EXPERIENCE"]
    ]):
        convert_line_id_to_id_node[line.id_line] = idx

    for line in document_page.full_lines:
        if line.label == label_name["WORK_EXPERIENCE"]:
            """get_adjacent_lines(line.lines_up, line, convert_line_id_to_id_node,
                               nodes, edges)"""
            get_adjacent_lines(line.lines_down, line,
                               convert_line_id_to_id_node, nodes, edges)
            """get_adjacent_lines(line.lines_left, line,
                               convert_line_id_to_id_node, nodes, edges)"""
            get_adjacent_lines(line.lines_right, line,
                               convert_line_id_to_id_node, nodes, edges)

    return [nodes, edges]
