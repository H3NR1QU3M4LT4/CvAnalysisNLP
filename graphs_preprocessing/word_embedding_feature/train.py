"""from transformers import TrainingArguments

from .metrics import compute_metrics
from .custom_trainer import CustomTrainer


def train(model, train_dataset, eval_dataset):

    training_args = TrainingArguments(output_dir='data/model/logs_model/',
                                      overwrite_output_dir = True,
                                      evaluation_strategy='steps',
                                      eval_steps=1,
                                      logging_steps = 5,
                                      num_train_epochs=1,
                                      metric_for_best_model='f1',
                                      logging_strategy = 'steps',
                                      report_to='tensorboard',
                                      save_strategy = 'steps',
                                      optim='adamw_torch',
                                      per_device_train_batch_size=12,
                                      per_device_eval_batch_size=12,
                                      warmup_steps=1,
                                      weight_decay=0.01,
                                      save_total_limit=1 )

    trainer = CustomTrainer(model=model,
                            args=training_args,
                            train_dataset=train_dataset,
                            eval_dataset=eval_dataset,
                            compute_metrics=compute_metrics)

    trainer.train()
    trainer.evaluate()
    trainer.save_model('data/model/best_model/')
    """