

from pathlib import Path
import spacy
from spacy.language import Language
from spacy.util import filter_spans
from spacy.tokens import Span
import typer 
import srsly
import re 
import pysbd
import sys, os 
from pysbd.utils import PySBDFactory

@Language.component("Find_LatexTable")
def Find_Latex_Table(doc):
    patterns = srsly.read_json("configs/regex_component.json")
    text = doc.text
    camp_ents = []
    original_ents = list(doc.ents)
    for label, pattern in patterns.items():
        for match in re.finditer(pattern, doc.text):
            start, end = match.span()
            span = doc.char_span(start, end)
            if span is not None:
                camp_ents.append((span.start, span.end, span.text))
        for ent in camp_ents:
            start, end, name = ent
            per_ent = Span(doc, start, end, label=label)
            original_ents.append(per_ent)
        filtered = filter_spans(original_ents)
        doc.ents = filtered
    return doc

@Language.component("pysbd_sentencizer")
def pysbd_sentence_boundaries(doc):
    seg = pysbd.Segmenter(language="fr", clean=False, char_span=True)
    sents_char_spans = seg.segment(doc.text)
    char_spans = [doc.char_span(sent_span.start, sent_span.end) for sent_span in sents_char_spans]
    start_token_ids = [span[0].idx for span in char_spans if span is not None]
    for token in doc:
        token.is_sent_start = True if token.idx in start_token_ids else False
    return doc
    
@Language.component("custom_sentencizer")
def set_custom_boundaries(doc):
    for token in doc[:-1]:
        if token.text in ["§","."]:
            #print("token.text", token.text)
            doc[token.i + 1].is_sent_start = True
    return doc

@Language.component("entity_retokenizer")
def set_entity_retokenizer_component(doc):
        with doc.retokenize() as retokenizer:
            for ent in doc.ents:
                retokenizer.merge(doc[ent.start:ent.end], attrs={"LEMMA": str(doc[ent.start:ent.end])})
        return doc



