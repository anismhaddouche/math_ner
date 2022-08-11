"""
@authors: Anne, Karim, Guillaume, Sébastien, Anis
"""

import json
import gzip
from bs4 import BeautifulSoup
import os
from pathlib import Path
import typer
import tqdm
import re

# def clean_text(html_txt):
#     # Elimine les balises html
#     # inspiré de https://stackoverflow.com/questions/22799990/beatifulsoup4-get-text-still-has-javascript
#     text = BeautifulSoup(html_txt, 'lxml').get_text()
#     lines = (line.strip() for line in text.splitlines())
#     chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
#     text = '\n'.join(chunk for chunk in chunks if chunk)
#     return text


def clean_text(text: str, regex: str):
    """
    Clean a text using a RegEx patterns. Note that the order of the RegEx expressions (patterns) is important.
    """
    with open(regex, mode="r") as f:
        patterns = json.load(f)

    # Extract latex equations and add '$' character at the beginning and at the end of each equation
    html_text = re.sub(patterns["DATA_KATEX"]["expression"], r"> $\1$ ", text)
    # Tag the end of html paragraphs
    html_text = re.sub(patterns["PARAGRAPH_END"]["expression"], r" § \1", html_text)
    # Extract table and add '&' character at the beginning and at the end of each table
    html_text = re.sub(patterns["DATA_TABLE"]["expression"], r" ¥¥\1\2\3¥¥ ", html_text)
    # Tag the end of cells
    html_text = re.sub(patterns["DATA_TABLE_CELL"]["expression"], r"¥\1", html_text)
    # Remove HTML tags
    cleaned_text = BeautifulSoup(html_text, "lxml").get_text()
    #  #### Replace " with '
    cleaned_text = cleaned_text.replace('"', "'")
    # Replace a consecutive repetition of '\n' character with white space
    cleaned_text = re.sub(
        patterns["NEW_LINES"]["expression"],
        r" ",
        BeautifulSoup(cleaned_text, "lxml").get_text(),
    )
    # Remove multiples Paragraphs end
    cleaned_text = re.sub(
        patterns["MULTIPLE_END_PARAGRAPHS"]["expression"], r"§", cleaned_text
    )
    # Remove doulbe §§ in the end of labdocs
    cleaned_text = re.sub(
        patterns["MULTIPLE_END_PARAGRAPHS_IN_END_LABDOC"]["expression"],
        r"",
        cleaned_text,
    )
    # Replace .§ with .
    cleaned_text = re.sub(
        patterns["PARAGRAPH_END-DOT"]["expression"], r".", cleaned_text
    )
    # Replace consecutive repetition of '.' character with a single '.'
    cleaned_text = re.sub(patterns["DOTS"]["expression"], r".", cleaned_text)
    # Delete '_' character to avoid problems like '______' with the tokenizer
    cleaned_text = re.sub(patterns["UNDERSCORES"]["expression"], r"", cleaned_text)
    # Replace a consecutive repetition of '\n' character with white space
    cleaned_text = re.sub(patterns["SPACES"]["expression"], r" ", cleaned_text)
    # Replace consecutive repetition of '-' character with a single '-'
    cleaned_text = re.sub(patterns["DASHES"]["expression"], r"-", cleaned_text)
    # Replace '\'  with '\\'
    cleaned_text = re.sub(patterns["BACKSLASH"]["expression"], r"\\\\", cleaned_text)
    # Replace for exemple ',mot'  with  ', mot '
    cleaned_text = re.sub(
        patterns["COMA_NUMBERS"]["expression"], r"\1.\3", cleaned_text
    )
    # Replace for example 'a=  b' by 'a=b'
    cleaned_text = re.sub(
        patterns["MATH_OP_EXTRA_SPACES"]["expression"], r"\1\2\3", cleaned_text
    )
    # For SI units like '1.5 m' which will be changed to '1.5m'
    cleaned_text = re.sub(
        patterns["SI_UNITS_SPACE"]["expression"], r"\1\2", cleaned_text
    )
    # Replace again a consecutive repetition of '\n' character with white space
    cleaned_text = re.sub(patterns["SPACES"]["expression"], r" ", cleaned_text)
    # Replace for example '( some_expression )' with '(some_expression )'
    cleaned_text = re.sub(
        patterns["BRACKETS_SPACES"]["expression"], r"\1\2\3", cleaned_text
    )
    # Replace for exemple 'mot ,' with 'mot,'
    cleaned_text = re.sub(
        patterns["WORD_SPACES_COMA-DOT"]["expression"], r"\1\2", cleaned_text
    )
    # Replace for exemple ',mot'  with  ', mot '
    cleaned_text = re.sub(patterns["COMA_WORD"]["expression"], r"\1 \2", cleaned_text)
    # Replace for exemple "word1:  word 2" by "word1 : word 2"
    cleaned_text = re.sub(patterns["WORD_COLON"]["expression"], r"\1 \2 ", cleaned_text)
    # Replace . § with .
    cleaned_text = re.sub(r"\.\s§", r".", cleaned_text)
    return cleaned_text


def extract_text(regex: str):
    """
    output: dict[id_report][id_labdoc] = list([text, user, id_trace])`
    exemple:
        {"29502":
           {"272580": [
              ["Les plus importantes...", "8514", 5541929],
              ["Les Plus importantes...", "8513", 5541935]]
           }
        }
    """
    typer.secho(
        f"-- Extract and clean text from labdoc according to regex patterns in {regex}",
        fg=typer.colors.GREEN,
    )

    # Get id's of initial labdocs texts
    with gzip.open("tmp/labdocs_texts_init.json.gz", "rt", encoding="utf-8") as zipfile:
        labdoc_text_init = json.load(zipfile)

    # Get id's of missions
    id_missions = [
        rep
        for rep in os.listdir("versioning")
        if os.path.isdir(os.path.join("versioning", rep))
    ]

    # pbar = tqdm.tqdm(total=len(id_missions),ascii=' >=',colour='green',desc='Missions')
    for id_mission in id_missions:
        data_out = {}
        path = "versioning/" + id_mission + "/"
        data_out = {}
        labdocs_filenames = [
            f
            for f in os.listdir(path)
            if os.path.isfile(os.path.join(path, f)) and not f.startswith(".")
        ]
        pbar = tqdm.tqdm(
            total=len(labdocs_filenames),
            ascii=" >=",
            colour="green",
            desc=f"Mission {id_mission}",
        )
        for labdoc_filename in labdocs_filenames:
            labdoc = str(int(labdoc_filename[:-8]))
            if labdoc in labdoc_text_init:
                # nb_labdocs += 1
                with gzip.open(
                    path + labdoc_filename, "rt", encoding="utf-8"
                ) as zipfile:
                    if zipfile:
                        data_in = json.load(zipfile)

                        id_report = data_in["id_report"]
                        id_labdoc = data_in["id_labdoc"]

                        if id_report not in data_out:
                            data_out[id_report] = {}

                        if id_labdoc not in data_out[id_report]:
                            data_out[id_report][id_labdoc] = []
                            # Etat initial
                            initial_html = labdoc_text_init[labdoc]
                            if initial_html:
                                initial_text = clean_text(initial_html, regex)
                                if initial_text:
                                    # data_out[id_report][id_labdoc].append([{'text':initial_text,'id_user':'ens','id_trace':0}])
                                    data_out[id_report][id_labdoc].append(
                                        [initial_text, "ens", 0]
                                    )

                        for content in data_in["contents"]:
                            id_user = content["id_user"]
                            id_trace = content["id_trace"]
                            html = content["data"]
                            if html:
                                text = clean_text(html, regex)
                                if text:
                                    # data_out[id_report][id_labdoc].append([{'text':text,'id_user':str(id_user),'id_trace':id_trace}])
                                    data_out[id_report][id_labdoc].append(
                                        [text, str(id_user), id_trace]
                                    )

                        if not data_out[id_report][id_labdoc]:
                            del data_out[id_report][id_labdoc]
            pbar.update(1)
        if data_out:
            Path("tmp/missions_texts").mkdir(parents=True, exist_ok=True)
            with gzip.open(
                f"tmp/missions_texts/{id_mission}.json.gz", "wt", encoding="utf-8"
            ) as zipfile:
                json.dump(data_out, zipfile, ensure_ascii=False, indent=-1)
        pbar.update(1)


if __name__ == "__main__":
    typer.run(extract_text)
