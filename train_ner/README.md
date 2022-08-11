<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Train a NER model with Spacy according to a Regex patterns

In this project, we train a NER model to detect entities in text Labdocs according to Regex Patterns. This model will be used (in other project) to improve annotation manually using Prodigy where the improved annotation will be used to train a new model.

## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[spaCy projects documentation](https://spacy.io/usage/projects).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `get_init` | Get all cleaned text Labdocs according to the regex patterns regex_text.json. We extract one Labdoc from each report. See the 'clean_text' function for more details about the applied clean. |
| `get_sample` | Get a sample of Labdocs with equations and table  |
| `get_train` | Get a sample of Labdocs according to the Regex patterns in regex_ner.json for training and testing a NER model from scratch |
| `create-config` | Create a config for replacing only NER from an existing pipeline |
| `train` | Train the NER model |
| `evaluate` | Evaluate the model and export metrics |
| `visualize-model` | Visualize the model's output interactively using Streamlit |
| `package-model` | Package the trained model as a pip package |
| `readme` | Create a readme file |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `get_labdocs` | `get_init` &rarr; `get_sample` &rarr; `get_train` &rarr; `create-config` |
| `train_ner` | `train` &rarr; `evaluate` &rarr; `readme` |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->