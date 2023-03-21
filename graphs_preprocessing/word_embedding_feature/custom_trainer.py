"""import torch
from torch import nn
import numpy as np
import pandas as pd
from transformers import Trainer
from sklearn.utils import class_weight


device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.get("labels")
        # forward pass
        outputs = model(**inputs)
        logits = outputs.get("logits")

        dataframe = pd.DataFrame(data=self.train_dataset.labels, columns = ['list_target_block_pair_lines'])

        sklearn_weights = class_weight.compute_class_weight(class_weight='balanced',
                                                            y=dataframe['list_target_block_pair_lines'],
                                                            classes=np.unique(dataframe['list_target_block_pair_lines'])).tolist()
        weights = torch.tensor(sklearn_weights)

        loss_fct = nn.CrossEntropyLoss(weight=weights.to(device))

        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss

"""