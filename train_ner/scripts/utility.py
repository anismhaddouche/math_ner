
import re 
from bs4 import BeautifulSoup
import mysql.connector as mariadb
from prodigy.components.db import connect
import typer 
import streamlit as st 
import jsonlines
import spacy
from spacy.tokens import Span
from tqdm import tqdm
import typer 
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
import sys 
from pathlib import Path


# def clean_text(text:str):
#     """
#     Clean a text using a RegEx patterns.
#     This function will be used in the get_assets() function
#     """
#     patterns = {
#                     "p1":[r'(\n)\s+|s\1+',r' '],                                                            #Replace a consecutive repetition of '\n' character with white space
#                     "p2":[r'(\.+)',r'.'],                                                                   #Replace consecutive repetition of '.' character with a single '.'
#                     "p3": [r'\s+',r' '],                                                                    #Replace consecutive repetition of white space with a single white space
#                     "p4": [r"(\-+)",r'-'],                                                                  #Replace consecutive repetition of '-' character with a single '-'
#                     "p6": [r"(_+)",r''],                                                                    #Delete '_' character to avoir problems like '______' with the tokenizer 
#                     "p5": [r'(\\)',r'\\\\'],                                                                #Replace '\' character with '\\'
#                     "p9": [r"(\d)(,)(\d)",r'\1.\3'],                                                        #Replace ',' by '.' in numbers
#                     "p10": [r"(.*?)\s{0,}(=|-|\+|\*|/|±|×|x|≈|÷|≠|≡|∼|≤|<|≪|≥|≫|∓|⋅|<=>)\s{0,}(.*?)",r'\1\2\3'],  #Replace for example 'a=  b' by 'a=b'
#                     "p6" : [r'(\d+)\s{1,}([\*]{0,}(10)|°C |[cdCDkKMmµGk]{0,}([mM]ol|[cC]d|m./.|Ω|µ|[Rr]ad|[oO]hm|H[zZ]|lm|lux|[kK]at|pa|kg|Gy|(N|J|W|A|V|C|T|F|H|K|g|s|m)\s))',r'\1\2'], # For SI units like '1.5 m' which will be changed to '1.5m' 
#                     "p11": [r"(\(|\[|\{)\s{0,}(.*?)\s{0,}(\}|\]|\))",r'\1\2\3'],                            #Replace for example '( some_expression )' with '(some_expression )'
#                     "p12" : [r"(\w)\s{1,}(,.|\..)",r'\1\2'],                                                #Replace for exemple 'mot ,' with 'mot,'
#                     "p13" : [r"(\,)([a-zA-Z])",r'\1 \2'   ],                                                #Replace for exemple ',mot'  with  ', mot ' 
#                     "p15" : [r'([a-zA-Z])(\:)\s+',r'\1 \2 ']                                                #Replace for exemple "word1:  word 2" by "word1 : word 2"

                    
#                 }
#     # Extract latex equations and add '$' character at the beginning and at the end of each equation
#     text = re.sub(r"data-katex=\"(.*?)\">",r'> $\1$ ',text)
#     # Extract table and add '&' character at the beginning and at the end of each table
#     text = re.sub(r"(<table)([\S\s]+)(table>)",r" ¥\1\2\3¥ ",text)
#     # Remove HTML tags
#     cleaned_text = BeautifulSoup(text, 'lxml').get_text()
#      #### Replace " with ' 
#     cleaned_text = cleaned_text.replace('"', "'")

#     cleaned_text = re.sub(patterns["p1"][0],patterns["p1"][1], BeautifulSoup(cleaned_text, 'lxml').get_text())
#     cleaned_text = re.sub(patterns["p2"][0],patterns["p2"][1], cleaned_text)
#     cleaned_text = re.sub(patterns["p3"][0],patterns["p3"][1], cleaned_text)
#     cleaned_text = re.sub(patterns["p4"][0],patterns["p4"][1], cleaned_text)
#     cleaned_text = re.sub(patterns["p5"][0],patterns["p5"][1], cleaned_text)
#     cleaned_text = re.sub(patterns["p9"][0],patterns["p9"][1], cleaned_text)
#     cleaned_text = re.sub(patterns["p10"][0],patterns["p10"][1], cleaned_text)
#     cleaned_text = re.sub(patterns["p6"][0],patterns["p6"][1], cleaned_text)
#     cleaned_text = re.sub(patterns["p3"][0],patterns["p3"][1], cleaned_text)
#     cleaned_text = re.sub(patterns["p11"][0],patterns["p11"][1], cleaned_text)
#     cleaned_text = re.sub(patterns["p12"][0],patterns["p12"][1], cleaned_text)
#     cleaned_text = re.sub(patterns["p13"][0],patterns["p13"][1], cleaned_text)
#     cleaned_text = re.sub(patterns["p15"][0],patterns["p15"][1], cleaned_text)

#     return cleaned_text

# def clean_text(text:str, regex:str):
#     """
#     Clean a text using a RegEx patterns.
#     This function will be used in the get_assets() function
#     """
#     with open(regex, mode='r') as f:
#         patterns = json.load(f)
   
#     # Extract latex equations and add '$' character at the beginning and at the end of each equation
#     html_text = re.sub(patterns["DATA_KATEX"]["regex"],r'> $\1$ ',text)
#     # Extract table and add '&' character at the beginning and at the end of each table
#     html_text = re.sub(patterns["DATA_TABLE"]["regex"],r" ¥\1\2\3¥ ",text)
#     # Remove HTML tags
#     text = BeautifulSoup(text, 'lxml').get_text()
#     #  #### Replace " with ' 
#     text = text.replace('"', "'")

#     #Replace a consecutive repetition of '\n' character with white space
#     cleaned_text = re.sub(patterns["NEW_LINES"]["regex"],r' ', text)  
#     #Replace consecutive repetition of '.' character with a single '.'
#     cleaned_text = re.sub(patterns["DOTS"]["regex"],r'.', cleaned_text)
#     #Delete '_' character to avoid problems like '______' with the tokenizer 
#     cleaned_text = re.sub(patterns["UNDERSCORES"]["regex"],r'', cleaned_text)
#     #Replace a consecutive repetition of '\n' character with white space
#     cleaned_text = re.sub(patterns["SPACES"]["regex"],r' ', cleaned_text)
#     #Replace consecutive repetition of '-' character with a single '-'
#     cleaned_text = re.sub(patterns["DASHES"]["regex"],r'-', cleaned_text)
#     #Replace '\'  with '\\'
#     cleaned_text = re.sub(patterns["BACKSLASH"]["regex"],r'\\\\', text)
#     #Replace for exemple ',mot'  with  ', mot '
#     cleaned_text = re.sub(patterns["COMA_NUMBERS"]["regex"],r'\1.\3', cleaned_text)
#     #Replace for example 'a=  b' by 'a=b'
#     cleaned_text = re.sub(patterns["MATH_OP_EXTRA_SPACES"]["regex"],r'\1\2\3', cleaned_text)
#     # For SI units like '1.5 m' which will be changed to '1.5m' 
#     cleaned_text = re.sub(patterns["SI_UNITS_SPACE"]["regex"],r'\1\2', cleaned_text)
#     #Replace again a consecutive repetition of '\n' character with white space
#     cleaned_text = re.sub(patterns["SPACES"]["regex"],r' ', cleaned_text)
#     #Replace for example '( some_expression )' with '(some_expression )'
#     cleaned_text = re.sub(patterns["BRACKETS_SPACES"]["regex"],r'\1\2\3', cleaned_text)
#     #Replace for exemple 'mot ,' with 'mot,'
#     cleaned_text = re.sub(patterns["WORD_SPACES_COMA-DOT"]["regex"],r'\1\2', cleaned_text)
#     #Replace for exemple ',mot'  with  ', mot '
#     cleaned_text = re.sub(patterns["COMA_WORD"]["regex"],r'\1 \2', cleaned_text) 
#     #Replace for exemple "word1:  word 2" by "word1 : word 2"
#     cleaned_text = re.sub(patterns["WORD_COLON"]["regex"],r'\1 \2 ', cleaned_text) 
#     return cleaned_text

#TODO : ecrire clean text que pour un seul pattern et boucler sur l'ensemble des patterns lors de l'appel de la fonct

def execute_query(user: str, host: str, database: str, password: str, query: str):
    """
    Execute a query in a database
    """
    try:
        conn = mariadb.connect(
            user = user,
            password = str(password),
            host = host ,
            database = database
        )
    except mariadb.Error as e:
        typer.secho(f"Error connecting to MariaDB Platform: {e}",fg=typer.colors.MAGENTA)
    cur = conn.cursor()
    cur.execute(query)
    table = cur.fetchall()
    cur.close()
    conn.close()
    return table 


def data_to_jsonl(data: list, path: str, filename: str):
    typer.secho(f'-- Save data in a JSONL file', fg=typer.colors.MAGENTA)
    #pbar = tqdm(total=len(data)) # Init pbar

    with open(f'{path}/{filename}.jsonl', 'w', encoding='utf-8') as file:
        for line in data:
            #file.write(f"{line}\n")
            file.write(f'{{\"text\":\"{line["text"]}\",\"meta\":{{\"id_labdoc\":\"{line["meta"]["id_labdoc"]}\",\"id_report\":\"{line["meta"]["id_report"]}\",\"id_mission\":\"{line["meta"]["id_mission"]}\"}}}}\n')
            #pbar.update(1)


# def update_doc_tokenizer(doc, patterns = {"latex_equation":  r"[$,\\\{,\\\[]{1,2}(.*?)[$,\\\},\\\]]{1,2}", "text_equation": r"(\s{0,}\S+=\S+\s{0,})"} ):
#     """
#     This function tokenize a text using the regex pattern and updates the Spacy doc object and  the "doc" tokenizer.
#     inputs:
#         patterns : A dictionary of regex patterns
#         doc : A Spacy doc object where type(doc) returns 'spacy.tokens.doc.Doc'
#         pattern : A regex pattern
#     outputs:
#         doc : A Spacy doc object updated with the new tokens
#     """
#     spans = []
#     for _, pattern in patterns.items():
#         for match in re.finditer(pattern, doc.text):
#             start, end = match.span()        
#             span = doc.char_span(start, end,alignment_mode = "expand") 
#             if span != None :
#                 spans.append(doc[span.start:span.end])        
#     filtred_spans = spacy.util.filter_spans(spans)  # Remove overlapping spans
#     with doc.retokenize() as retokenizer:
#         for span in filtred_spans:
#                 #print(span)
#                 retokenizer.merge(span)
#     return doc

# def extract_formula_tokenizer(doc, patterns = {"LATEX_MATH":  r"[$]{1,2}(.*?)[$]{1,2}", "TEXT_MATH": r"(\s\S+=\S+\s)"} ):
#     """
#     This function tokenize a text using the regex pattern and updates the Spacy doc object and  the "doc" tokenizer.
#     inputs:
#         patterns : A dictionary of regex patterns
#         doc : A Spacy doc object where type(doc) returns 'spacy.tokens.doc.Doc'
#         pattern : A regex pattern
#     outputs:
#         doc : A Spacy doc object updated with the new tokens
#     """
#     spans = [] 
#     orig_ents = list(doc.ents)
#     print(orig_ents)
#     for label, regex in patterns.items():
#         for match in re.finditer(regex, doc.text):
#             start, end = match.span()        
#             span = doc.char_span(start, end,label=label,alignment_mode = "expand") 
#             if span != None :
#                 spans.append(doc[span.start:span.end])   
#                 doc.set_ents([Span(doc, span.start, span.end, label)],default="unmodified") # add the new span to the doc
#     filtred_spans = spacy.util.filter_spans(spans)              # Remove overlapping spans
#     with doc.retokenize() as retokenizer:                       # Retokenize the filtered spans
#         for span in filtred_spans:
#                 #print(span)
#                 retokenizer.merge(span)
#     return doc


# def get_sample_train(nlp, input:str, output:str):
#     """
#     This function returns a sample train data with annotated formula (TEXT and LATEX).
#     inputs:
#         nlp : A Spacy nlp object
#         input : A string containing the input text
#         output : A string containing the output text
#     outputs:
        
#     """
#     TRAIN_DATA = []
#     with open(input+".jsonl", "r",encoding='utf-8') as f:
#         for line in f:
#             doc = nlp(json.loads(line)["text"])
#             doc = extract_formula_tokenizer(doc)
#             TRAIN_DATA.append([doc.text, {"entities": [(e.start_char, e.start_char, e.label_) for e in doc.ents ]  }])
#     with open(output+"_spacy.jsonl", "w",encoding='utf-8') as f:
#         for line in TRAIN_DATA:
#             f.write(json.dumps(line,ensure_ascii=False) + "\n")

def get_prodigy_dataset(data_set_name : str, db = connect()):
    """
    Get data from Prodigy database
    outputs:  A list of dictionaries
    """
    # from prodigy.components.db import connect
    # import typer 
    try :
        db 
    except Exception as e:
        typer.secho(e, fg="red")
        return None
    try :
        dataset = db.get_dataset(data_set_name)
        typer.secho(f'√ The dataset {data_set_name} of size {db.count_dataset(data_set_name)} was successfully uploaded ', fg="green")
    except Exception as e:
        typer.secho(e,fg="red")
        return None
    return dataset

