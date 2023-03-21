from label_name_enum.label_name_enum import label_name


def connect_all_nodes(lines, line, convert_line_id_to_id_node, nodes,
                       edges):
    for idx, remainig_line in enumerate(lines):
        if remainig_line.label == label_name["WORK_EXPERIENCE"]:
            if line != lines[idx]:
                nodes.append(convert_line_id_to_id_node[line.id_line])
                edges.append(
                    convert_line_id_to_id_node[remainig_line.id_line])
            

def connect_edge_target_all_nodes(lines, line, convert_line_id_to_id_node, nodes,
                       edges):
    for idx, remainig_line in enumerate(lines):
        if remainig_line.label == label_name["WORK_EXPERIENCE"]:
            if remainig_line.block:
                if line.block.id_block == remainig_line.block.id_block:
                    if line != lines[idx]:
                        nodes.append(convert_line_id_to_id_node[line.id_line])
                        edges.append(
                            convert_line_id_to_id_node[remainig_line.id_line])
                    