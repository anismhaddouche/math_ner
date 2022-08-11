
import spacy 
from spacy.util import registry, compile_prefix_regex
from spacy.tokenizer import Tokenizer
import re 



@registry.callbacks("customize_tokenizer")
def make_customize_tokenizer():
    def customize_tokenizer(nlp):
        added_prefix = nlp.Defaults.suffixes +  [r'''\w\'\w+''',]
        prefix_regex = spacy.util.compile_prefix_regex(added_prefix)
        nlp.tokenizer.prefix_search = prefix_regex.search
    return customize_tokenizer



