# get the devtrain set from the prodigy database 
from pathlib import Path
from prodigy.components.db import connect
import typer 
import jsonlines
import spacy
from spacy.tokens import DocBin
from spacy.util import filter_spans
import warnings

def is_whitespace_entity(text):
    whitespace = (" ", "\n")  # etc.
    if text.startswith(whitespace) or text.endswith(whitespace):
        return True
    for char in whitespace:
        if text == char:
            return True
    return False

def get_data_from_db(lang:str, dataset : str ):
    """
    Connecte the prodigy database of annotation and get the annotated file in a spacy format 
    """
    typer.secho(f'--- Get the data from the prodigy database', fg=typer.colors.BRIGHT_BLUE)
    db = connect()
    if dataset not in db.datasets : 
        typer.secho(f'--- The dataset {dataset} does not exist in the prodigy database', fg=typer.colors.RED)
        return
    else :
        typer.secho(f'--- The dataset {dataset} exist in the prodigy database', fg=typer.colors.GREEN)
    nlp = spacy.blank(lang)
    data = db.get_dataset(dataset)
    doc_bin = DocBin()
    with jsonlines.open(f"assets/{dataset}.jsonl", mode='w') as writer:
        for line in data :
            doc = nlp(line["text"])
            entities = []
            ents = []
            for ent in line['spans']:
                entities.append([ent['start'], ent['end'], ent['label']])
            new_line = {"text":line["text"], "entities":entities,"meta":line["meta"]}
            writer.write(new_line)

            for start, end, label in entities:
                span = doc.char_span(start, end, label=label)
                if span is None:
                    msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries"
                    warnings.warn(msg)
                else:
                    entity = doc.text[start:end] # get the entity 
                    # ents.append(span)  
                    if not is_whitespace_entity(entity): # if the entity is not a whitespace with is depreciated in the spacy train
                        ents.append(span)
            doc.ents = filter_spans(ents)
            if doc.ents != ():
                doc_bin.add(doc)

    doc_bin.to_disk(f"corpus/{dataset}.spacy")        
    


#get_data_from_db("fr","/Users/anis/test_labnbook/math_ner/correct_annotation/assets/dev.jsonl", "dev_corrected")

if __name__ == "__main__":
    typer.run(get_data_from_db)