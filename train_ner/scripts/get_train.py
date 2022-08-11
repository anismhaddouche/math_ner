import random
import srsly
from pathlib import Path
import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans
from spacy.tokens import Span
import json 
import re 
import warnings
from tqdm import tqdm
import typer 
import pandas as pd
import wandb
from prettytable import PrettyTable


def is_whitespace_entity(text):
    whitespace = (" ", "\n")  # etc.
    if text.startswith(whitespace) or text.endswith(whitespace):
        return True
    for char in whitespace:
        if text == char:
            return True
    return False

# def get_ents(lang:str, input : list, outputs_name: str, patterns_file : Path):
#     """
#     get the entities, using the regex patterns_file , from an input jsonl file and save it to a json file and a Spacy file
#     """
#     typer.secho(f'--- Extract and convert entities to construct the {outputs_name} set', fg=typer.colors.BRIGHT_BLUE)

#     patterns = srsly.read_json(patterns_file)
#     nlp = spacy.blank(lang)
#     DATA = []
#     doc_bin = DocBin() # for storing the entities
#     del_doc = 0 # for counting the number of documents with no entities
#     pbar = tqdm(total=len(input),ascii=' >=')
#     for line in input: # for each document
#         ents = [] 
#         doc = nlp(line["text"])
#         for label, regex in patterns.items(): # for each pattern
#             for match in re.finditer(regex, doc.text): # for each match of the pattern
#                 start, end = match.span()         # get the start and end position of the match
#                 span = doc.char_span(start, end,label=label,alignment_mode = "expand")  # get the span of the match
#                 if span != None :  # if the span is not None
#                     entity = doc.text[start:end] # get the entity 
#                     # ents.append(span)  
#                     if not is_whitespace_entity(entity): # if the entity is not a whitespace with is depreciated in the spacy train
#                         ents.append(span)
                    
#                 else : 
#                     msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
#                     warnings.warn(msg)
#         doc.ents = filter_spans(ents)
#         if doc.ents != (): # if the doc has entities
#             DATA.append([doc.text, {"entities": [(e.start_char, e.end_char, e.label_) for e in doc.ents ]  }])
#             # #count labels of a doc 
#             # doc_labels = [e.label_ for e in doc.ents]
#             # doc_labels_nb = {label : doc_labels.count(label) for label in doc_labels}
#             # # count sum of distinct labels of a doc_labels_nb
#             # #print(doc_labels_nb)
#             doc_bin.add(doc) # add the doc to the doc_bin
#         else : 
#             del_doc += 1 # count the number of docs with no entities
#         pbar.update(n=1)

#     if del_doc != 0 :
#         typer.secho(f"---- {del_doc} documents ({round(del_doc/len(input),2)}%) were deleted because they contain entities with whitespace characters which is depreciated by the Spacy train fuction", fg=typer.colors.RED)

#     with open(f"assets/{outputs_name}.json", "w",encoding='utf-8') as f: # save the data to a json file
#         json.dump(DATA,f,ensure_ascii=False,indent=4)
#     doc_bin.to_disk(f"corpus/{outputs_name}.spacy") # save the doc_bin to a Spacy file




# def get_train(lang:str, input: Path, train_size : float, patterns_file : Path):
#     """
#     This function returns a sample train data with named entities.
#     """  
#     typer.secho(f'-- Extract a sample of {train_size} labdocs containing tables, formula and their char position in the text', fg=typer.colors.BRIGHT_BLUE)
#     ALL_DATA = []
#     for line in srsly.read_jsonl(input):
#         ALL_DATA.append(line)
#     random.shuffle(ALL_DATA)
#     TRAIN_DATA = ALL_DATA[:int(len(ALL_DATA)*train_size)]
#     DEV_DATA = ALL_DATA[int(len(ALL_DATA)*train_size):]
#     get_ents("fr", TRAIN_DATA, "train", patterns_file)
#     get_ents("fr", DEV_DATA, "dev", patterns_file)




def get_ents(lang:str, input : list, outputs_name: str, patterns_file : Path):
    """
    get the entities, using the regex patterns_file , from an input jsonl file and save it to a json file and a Spacy file
    """
    typer.secho(f'--- Extract and convert entities to construct the {outputs_name} set', fg=typer.colors.BRIGHT_BLUE)

    patterns = srsly.read_json(patterns_file)
    nlp = spacy.blank(lang)
    DATA = []
    labels = []
    doc_bin = DocBin() # for storing the entities
    del_doc = 0 # for counting the number of documents with no entities
    pbar = tqdm(total=len(input),ascii=' >=')
    for line in input: # for each document
        ents = [] 
        doc = nlp(line["text"])
        for label, regex in patterns.items(): # for each pattern
            for match in re.finditer(regex, doc.text): # for each match of the pattern
                start, end = match.span()         # get the start and end position of the match
                span = doc.char_span(start, end,label=label,alignment_mode = "expand")  # get the span of the match
                if span != None :  # if the span is not None
                    entity = doc.text[start:end] # get the entity 
                    # ents.append(span)  
                    if not is_whitespace_entity(entity): # if the entity is not a whitespace with is depreciated in the spacy train
                        ents.append(span)
                    
                else : 
                    msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                    warnings.warn(msg)
        doc.ents = filter_spans(ents)
        labels.append([e.label_ for e in doc.ents])
        if doc.ents != (): # if the doc has entities
            DATA.append([doc.text, {"entities": [(e.start_char, e.end_char, e.label_) for e in doc.ents ]},line["meta"]])
            doc_bin.add(doc) # add the doc to the doc_bin
        else : 
            del_doc += 1 # count the number of docs with no entities
        pbar.update(n=1)

    if del_doc != 0 :
        typer.secho(f"---- {del_doc} documents ({round(del_doc/len(input),2)}%) were deleted because they contain entities with whitespace characters which is depreciated by the Spacy train fuction", fg=typer.colors.RED)
    doc_bin.to_disk(f"corpus/{outputs_name}.spacy") # save the doc_bin to a Spacy file
    # Save as a json file  correcte the entities  with prodigy
    with open(f"assets/{outputs_name}.jsonl", "w",encoding='utf-8') as f:
        for line in DATA:
            new_line = {"text":line[0],"entities":line[1]["entities"],"meta":line[2]}
            #print(new_line["entities"])
            #print(new_line, type(line))
            f.write(json.dumps(new_line,ensure_ascii=False)+"\n")
    # Print the numbers of labels in data 

    artifact = wandb.Artifact('Total_Entities', {outputs_name})


    # for label in patterns.keys():
    #     total_labels = sum(labels, []).count(label) 
    total_labels = PrettyTable()
    total_labels.field_names = ["Entities", "Total"]
    for label in patterns.keys():
        #print(label, labels.count(label))
        total_labels.add_row([label, sum(labels, []).count(label)])
    return total_labels



def get_train(lang:str, input: Path, train_size : float, patterns_file : Path):
    """
    This function returns a sample of dev and train data with named entities.
    input : a jsonl file
    """  
    typer.secho(f'-- Extract a sample of {train_size} labdocs containing tables, formula and their char position in the text', fg=typer.colors.BRIGHT_BLUE)
    ALL_DATA = []
    for line in srsly.read_jsonl(input):
        ALL_DATA.append(line)

    # 
    random.shuffle(ALL_DATA)

    TRAIN_DATA = ALL_DATA[:int(len(ALL_DATA)*train_size)]
    DEV_DATA = ALL_DATA[int(len(ALL_DATA)*train_size):]

    total_labels_TRAIN = get_ents("fr", TRAIN_DATA, "train", patterns_file)

    
    
    print(total_labels_TRAIN)
    total_labels_DEV = get_ents("fr", DEV_DATA, "dev", patterns_file)
    print(total_labels_DEV)






# get_train("fr", "/Users/anis/test_labnbook/math_ner/get_annotate_convert_assets/source/labdoc_init_sample.jsonl", 0.8, "/Users/anis/test_labnbook/math_ner/get_annotate_convert_assets/configs/regex_ner.json")

if __name__ == "__main__":
    typer.run(get_train)





