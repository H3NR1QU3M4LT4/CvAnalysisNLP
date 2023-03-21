import torch
from torch_geometric.data import Data

from .edge_index import edge_index, edge_index_all_connected
from .edge_index_target import edge_index_target, edge_index_target_all_connected
from .features import graph_features
from .edge_attr import edge_attr, edge_attr_all_connected


def create_target(edge_index_array_tensor, edge_index_target_array_tensor):
    list_of_edges_in_output = [
        edge_index_target_array_tensor[:, i].tolist()
        for i in range(edge_index_target_array_tensor.shape[-1])
    ]
    boolean_edges_in_output = [
        edge_index_array_tensor[:, j].tolist() in list_of_edges_in_output
        for j in range(edge_index_array_tensor.shape[-1])
    ]

    return boolean_edges_in_output


def create_tensors_from_lines_data(dataset_lines_with_blocks, path):
    all_data = []
    for document in dataset_lines_with_blocks:
        for page in document.pages:
            if page.blocks != None:
                if len(page.blocks) != 0:
                    edge_index_array = edge_index(page)
                    edge_index_target_array = edge_index_target(page)
                    features_array = graph_features(document, page)
                    edge_attr_array = edge_attr(page)
                    
                    edge_index_tensor = torch.tensor(edge_index_array,
                                                     dtype=torch.long)
                    edge_index_target_array_tensor = torch.tensor(
                        edge_index_target_array, dtype=torch.long)
                    features_tensor = torch.tensor(features_array,
                                                   dtype=torch.float)
                    edge_attr_tensor = torch.tensor(edge_attr_array, dtype=torch.float)

                    target = create_target(edge_index_tensor,
                                           edge_index_target_array_tensor)
                    target_tensor = torch.tensor(target, dtype=torch.long)

                    data = Data(x=features_tensor,
                                edge_index=edge_index_tensor,
                                y=target_tensor,
                                edge_attr=edge_attr_tensor)
                    
                    all_data.append(data)

    return all_data


def create_tensors_from_all_nodes_connected(dataset_lines_with_blocks, path):
    all_data_nodes_connected = []
    for document in dataset_lines_with_blocks:
        for page in document.pages:
            if page.blocks != None:
                if len(page.blocks) != 0:
                    edge_index_array = edge_index_all_connected(page)
                    edge_index_target_array = edge_index_target_all_connected(page)
                    features_array = graph_features(document, page)
                    edge_attr_array = edge_attr_all_connected(page)
                    
                    edge_index_tensor = torch.tensor(edge_index_array,
                                                     dtype=torch.long)
                    edge_index_target_array_tensor = torch.tensor(
                        edge_index_target_array, dtype=torch.long)
                    features_tensor = torch.tensor(features_array,
                                                   dtype=torch.float)
                    edge_attr_tensor = torch.tensor(edge_attr_array, dtype=torch.float)

                    target = create_target(edge_index_tensor,
                                           edge_index_target_array_tensor)
                    target_tensor = torch.tensor(target, dtype=torch.long)

                    data = Data(x=features_tensor,
                                edge_index=edge_index_tensor,
                                y=target_tensor,
                                edge_attr=edge_attr_tensor)
                    
                    all_data_nodes_connected.append(data)

    return all_data_nodes_connected