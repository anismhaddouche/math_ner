#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Anne, Karim, Guillaume, Sébastien, Anis
"""

import json
import gzip
# import pysbd
from pathlib import Path
from lib import diff
import typer
import tqdm as tqdm
import sys, os 

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/model/fr_LabnbookNer-0.0.0'))
from components import *

nlp = spacy.load("model/fr_LabnbookNer-0.0.0")



def get_meta(doc):
    """
    Get the position of entities and punctuation token's mark
    output : {'ENTS':{'label1':[[star,end],[star,end]...],'label2 : [[star,end],[star,end],...]},'PUNCT':[pos1,pos2,...]}
    """
    # output = dict.fromkeys(list(ent.label_ for ent in doc.ents))
    # for label in output.keys():
    #     output[label]= []
    #     for ent in doc.ents :
    #         if ent.label_ == label :
    #             output[label].append([ent.start, ent.end])

    # punct_pos  = []
    # for token in doc :
    #     if token.is_punct :
    #         punct_pos.append([token.i])
    #  #add a key to the dict for punctuation
    # output = {'ENTS': output, 'PUNCT': punct_pos}

    segments = []
    tokens = []
    nb_tokens = 0
    start = 0
    # Get the start and end token position of each segment
    for seg in doc.sents:
        for token in seg:
            # tokens = [token.text for token in seg ]
            if not token.is_punct:
                tokens.append(token.text)
                nb_tokens += 1
        if nb_tokens == 0:
            segments = []
        else:
            end = nb_tokens - 1
            segments.append([start, end])
            start = end + 1
    #
    output = {}
    output["SEGS"] = segments
    output["NB_SEGS"] = len(segments)
    # # Get the number of tokens
    # # Get tokens
    output["TOKS"] = tokens
    output["NB_TOKS"] = nb_tokens
    return output


def contrib_and_segmentation():
    """
    output :
    dict[id_report][id_labdoc] = list([text, user, id_trace])
    example :
    {"29502":
        {"272580": [
      ["Les plus importantes...", "8514", 5541929],
      ["Les Plus importantes...", "8513", 5541935]]
         }
    }

    """
    typer.secho(
        "-- Execution of the contribution and segmentation algorithm ",
        fg=typer.colors.GREEN,
    )
    # Get a list of all mission
    id_missions = [
        rep[:-8] for rep in os.listdir("tmp/missions_texts/") if not rep.startswith(".")
    ]
    # pbar = tqdm.tqdm(total=len(id_missions),ascii=' >=',colour='green',desc='Missions')
    for id_mission in id_missions:
        data_out = {}
        # Get the path of each mission
        path = "tmp/missions_texts/" + id_mission + ".json.gz"
        # print(f"--- Calcul de contribution : traitement de la mission {id_mission} ---")
        # data_out = {}
        # Open the mission
        with gzip.open(path, "rt", encoding="utf-8") as zipfile:
            # Load the mission
            if zipfile:
                data_in = json.load(zipfile)
                # Loop on each report of the mission
                pbar = tqdm.tqdm(
                    total=len(data_in),
                    ascii=" >=",
                    colour="green",
                    desc=f"Mission {id_mission}",
                )
                for id_report in data_in:
                    data_out[id_report] = {}
                    # Loop on each labdoc of the report
                    for id_labdoc in data_in[id_report]:
                        data_out[id_report][id_labdoc] = []
                        list_of_text_user_id_trace = data_in[id_report][id_labdoc]
                        # Tokenize the text
                        list_of_text_user_id_trace = [
                            (text, user, id_trace)
                            for (text, user, id_trace) in list_of_text_user_id_trace
                        ]
                        contribution = [[], [[]], []]
                        # Loop on each version of the labdoc
                        for text_user_id_trace in list_of_text_user_id_trace:
                            doc = nlp(text_user_id_trace[0])
                            meta = get_meta(doc)
                            tokens = meta["TOKS"]
                            # tokens = [token.text for token in doc]
                            text_user = (tokens, str(text_user_id_trace[1]))
                            id_trace = text_user_id_trace[-1]
                            contribution = diff.one_step_contribution(
                                contribution, text_user, debug=False
                            )
                            users = diff.get_users(contribution)
                            # text = diff.get_words(contribution)
                            collab_matrix = diff.get_matrix(contribution)

                            segments = meta["SEGS"]
                            data_out[id_report][id_labdoc].append(
                                [users, collab_matrix, id_trace, meta]
                            )
                    pbar.update(1)

        Path("tmp/missions_contribs").mkdir(parents=True, exist_ok=True)
        with gzip.open(
            f"tmp/missions_contribs/{id_mission}.json.gz", "wt", encoding="utf-8"
        ) as zipfile:
            json.dump(data_out, zipfile, ensure_ascii=False, indent=2)

        # pbar.update(1)


if __name__ == "__main__":
    typer.run(contrib_and_segmentation)
