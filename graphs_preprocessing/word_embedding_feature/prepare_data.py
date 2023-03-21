"""import torch
from sklearn.model_selection import train_test_split

from .load_pretrained_model import tokenizer


def split_dataframe(dataframe):
    train_sentences_x, val_sentences_x, train_sentences_y, val_sentences_y, train_labels, val_labels = train_test_split(
        dataframe["line_x_text"].tolist(), 
        dataframe["line_y_text"].tolist(), 
        dataframe["list_target_block_pair_lines"].tolist(), 
        test_size=.2
    )
    
    return train_sentences_x, val_sentences_x, train_sentences_y, val_sentences_y, train_labels, val_labels


def encode_inputs(train_sentences_x, val_sentences_x, train_sentences_y, val_sentences_y):
    train_encodings = tokenizer(train_sentences_x, train_sentences_y, truncation=True, padding='max_length', max_length=128)
    val_encodings = tokenizer(val_sentences_x, val_sentences_y, truncation=True, padding='max_length', max_length=128)

    return train_encodings, val_encodings


class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

    
def create_datasets_for_training(dataframe):
    train_sentences_x, val_sentences_x, train_sentences_y, val_sentences_y, train_labels, val_labels = split_dataframe(dataframe)
    train_encodings, val_encodings = encode_inputs(train_sentences_x, val_sentences_x, train_sentences_y, val_sentences_y)
    
    train_dataset = Dataset(train_encodings, train_labels)
    val_dataset = Dataset(val_encodings, val_labels)

    return train_dataset, val_dataset
"""