<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project:  Correct annotated data with prodigy for NER

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
| `test1` | Test |
| `correct__dev` |  correcte the annotated data in sources/dev.jsonl  |
| `correct__train` | correcte the annotated data in sources/train.jsonl  |
| `get_dev_corrected` | get the corrected dev dataset  from prodigy database |
| `get_train_corrected` | get the corrected train dataset  from prodigy database in  |
| `create-config` | Create a config for replacing only NER from an existing pipeline |
| `train` | Train the NER model |
| `evaluate` | Evaluate the model and export metrics |
| `add_components` | Add the components to the model |
| `package-model` | Package the trained model as a pip package |
| `visualize-model` | Visualize the model's output interactively using Streamlit |
| `readme` | Create a readme file |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `correct_dev` | `correct__dev` |
| `correct_train` | `correct__train` |
| `get_devtrain_from_db` | `get_dev_corrected` &rarr; `get_train_corrected` |
| `correct_ner` | `create-config` &rarr; `train` &rarr; `evaluate` &rarr; `add_components` &rarr; `package-model` &rarr; `readme` |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->