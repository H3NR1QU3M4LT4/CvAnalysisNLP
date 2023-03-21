"""import os
import torch
from .prepare_data import create_datasets_for_training
from .load_pretrained_model import tokenizer, model
from .train import train
from .load_pretrained_model import model
from transformers import BertTokenizer, BertForNextSentencePrediction
import torch.nn.functional as F


device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


def create_new_feature(dataframe) -> list:
    if not os.path.exists('data/model/best_model/'):
        print(os.path.exists('data/model/best_model/'))
        train_dataset, val_dataset = create_datasets_for_training(dataframe)
        train(model, train_dataset, val_dataset)
    
    
    trained_model = BertForNextSentencePrediction.from_pretrained('data/model/best_model/')
        
    bert_probs = []
    for index, row in dataframe.iterrows():
        encoded_inputs = tokenizer(row['line_x_text'], row['line_y_text'], return_tensors="pt").to(device)
        outputs = trained_model(**encoded_inputs, labels=torch.LongTensor([1]).to(device))
        logits = outputs.logits
        probs = F.softmax(outputs.logits, dim=1)
        bert_probs.append(probs[0][1].tolist())
    
    return bert_probs
"""