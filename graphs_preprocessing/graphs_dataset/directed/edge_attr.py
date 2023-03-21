from label_name_enum.label_name_enum import label_name


def calculate_edge_features(line_x, line_y):
    distance_x1 = line_x.b_box.x1 - line_y.b_box.x1
    distance_x2 = line_x.b_box.x2 - line_y.b_box.x2
    distance_y1 = line_x.b_box.y1 - line_y.b_box.y1
    distance_y2 = line_x.b_box.y2 - line_y.b_box.y2
    return [distance_x1, distance_x2, distance_y1, distance_y2]
    

def get_edge_features(position_lines, line, edge_features):
    if position_lines:
        for positioned_line in position_lines:
            if positioned_line.label == label_name["WORK_EXPERIENCE"]:
                edge_features.append(calculate_edge_features(line, positioned_line))


def edge_attr(document_page):
    all_edges_features = []
    
    for line in document_page.full_lines:
        if line.label == label_name["WORK_EXPERIENCE"]:
            #get_edge_features(line.lines_up, line, all_edges_features)
            get_edge_features(line.lines_down, line, all_edges_features)
            #get_edge_features(line.lines_left, line, all_edges_features)
            get_edge_features(line.lines_right, line, all_edges_features)
    
    return all_edges_features
