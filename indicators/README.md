<!-- SPACY PROJECT: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 spaCy Project: Compute two indicators for each Labdoc version

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
| `extract_labdoc_text_init` | Get the id of text labdocs as well as the initial texts (with html tags) written by teachers. These step need an access to the local database  LabNbook |
| `extract_labdoc_text` | Extracts the text of each version of labdoc by removing the html tags and clean texts according to regex patterns. |
| `contrib_and_segmentation` |  |
| `collaboration` |  |
| `report` | Compute some reports about the indicators for each labdoc. |
| `readme` | Create a readme file |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`spacy project run [name]`](https://spacy.io/api/cli#project-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `extract_labdoc_text_versions` | `extract_labdoc_text_init` &rarr; `extract_labdoc_text` |
| `compute_contributions_matrices` | `contrib_and_segmentation` &rarr; `collaboration` &rarr; `report` &rarr; `readme` |

<!-- SPACY PROJECT: AUTO-GENERATED DOCS END (do not remove) -->