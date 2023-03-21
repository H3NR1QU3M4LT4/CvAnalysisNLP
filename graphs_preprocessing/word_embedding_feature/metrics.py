"""import numpy as np
from datasets import load_metric


glue_metric = load_metric('glue', 'mrpc')
return_entity_level_metrics = False

def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=1)

    # Remove ignored index (special tokens)
    true_predictions = [p for (p, l) in zip(predictions, labels)]

    true_labels = [l for (p, l) in zip(predictions, labels)]

    results = glue_metric.compute(predictions=true_predictions, references=true_labels)

    return results"""