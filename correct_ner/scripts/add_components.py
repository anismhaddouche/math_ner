

# from pathlib import Path
# import spacy
# from spacy.language import Language
# from spacy.util import filter_spans
# from spacy.tokens import Span
# import typer 
# import srsly
# import pysbd
from components import * 


def add_components(model : Path):
    """
    Add  components to the best model according to a Regex patterns file and save it to a new model
    """
    typer.secho(f"-- Adding components to the best model '{model}' according to a Regex patterns file and save it as '{model}'", fg=typer.colors.BRIGHT_BLUE)
    nlp = spacy.load(model)
    nlp.add_pipe("Find_LatexTable", before="ner")
    nlp.add_pipe("pysbd_sentencizer",before="ner")
    nlp.add_pipe("custom_sentencizer")
    nlp.add_pipe("entity_retokenizer")
    nlp.to_disk(model)
    



if __name__ == "__main__":
       typer.run(add_components)
#add_components("correct_ner/training/model-best")
# nlp = spacy.load("correct_ner/training/model-best-updated")
# #doc = nlp('This is a test sentence.')
# print(nlp.pipe_names)
