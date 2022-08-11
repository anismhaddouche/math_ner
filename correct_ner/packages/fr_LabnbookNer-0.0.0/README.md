| Feature | Description |
| --- | --- |
| **Name** | `fr_LabnbookNer` |
| **Version** | `0.0.0` |
| **spaCy** | `>=3.2.4,<3.3.0` |
| **Default Pipeline** | `tok2vec`, `Find_LatexTable`, `pysbd_sentencizer`, `ner`, `custom_sentencizer` |
| **Components** | `tok2vec`, `Find_LatexTable`, `pysbd_sentencizer`, `ner`, `custom_sentencizer` |
| **Vectors** | 0 keys, 0 unique vectors (0 dimensions) |
| **Sources** | n/a |
| **License** | n/a |
| **Author** | [n/a]() |

### Label Scheme

<details>

<summary>View label scheme (4 labels for 1 components)</summary>

| Component | Labels |
| --- | --- |
| **`ner`** | `LATEX_MATH`, `TABLE`, `TEXT_MATH`, `VALUE` |

</details>

### Accuracy

| Type | Score |
| --- | --- |
| `ENTS_F` | 48.02 |
| `ENTS_P` | 50.33 |
| `ENTS_R` | 45.92 |
| `TOK2VEC_LOSS` | 150852.44 |
| `NER_LOSS` | 276933.32 |