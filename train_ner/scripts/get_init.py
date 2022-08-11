import typer 
from pathlib import Path
from utility import *
import json
from tqdm import tqdm

def clean_text(text:str, regex:str):
    """
    Clean a text using a RegEx patterns. Note that the order of the RegEx expressions (patterns) is important.
    This function will be used in the get_assets() function
    """
    with open(regex, mode='r') as f:
        patterns = json.load(f)
   
    # Extract latex equations and add '$' character at the beginning and at the end of each equation
    html_text = re.sub(patterns["DATA_KATEX"]["expression"],r'> $\1$ ',text)
    # Tag the end of html paragraphs
    html_text = re.sub(patterns["PARAGRAPH_END"]["expression"],r' § \1',html_text)
    # Extract table and add '&' character at the beginning and at the end of each table
    html_text = re.sub(patterns["DATA_TABLE"]["expression"],r" ¥¥\1\2\3¥¥ ",html_text)
    # Tag the end of cells
    html_text = re.sub(patterns["DATA_TABLE_CELL"]["expression"],r"¥\1",html_text)
    # Remove HTML tags
    cleaned_text = BeautifulSoup(html_text, 'lxml').get_text()

    #  #### Replace " with ' 
    cleaned_text = cleaned_text.replace('"', "'")
    #Replace a consecutive repetition of '\n' character with white space
    cleaned_text = re.sub(patterns["NEW_LINES"]["expression"],r' ', BeautifulSoup(cleaned_text, 'lxml').get_text())  
    # Remove multiples Paragraphs end
    cleaned_text = re.sub(patterns["MULTIPLE_END_PARAGRAPHS"]["expression"],r'§', cleaned_text)    
    # Remove doulbe §§ in the end of labdocs 
    cleaned_text = re.sub(patterns["MULTIPLE_END_PARAGRAPHS_IN_END_LABDOC"]["expression"],r'', cleaned_text)
    # Replace .§ with .
    cleaned_text = re.sub(patterns["PARAGRAPH_END-DOT"]["expression"],r'.', cleaned_text)
    #Replace consecutive repetition of '.' character with a single '.'
    cleaned_text = re.sub(patterns["DOTS"]["expression"],r'.', cleaned_text)
    #Delete '_' character to avoid problems like '______' with the tokenizer 
    cleaned_text = re.sub(patterns["UNDERSCORES"]["expression"],r'', cleaned_text)
    #Replace a consecutive repetition of '\n' character with white space
    cleaned_text = re.sub(patterns["SPACES"]["expression"],r' ', cleaned_text)
    #Replace consecutive repetition of '-' character with a single '-'
    cleaned_text = re.sub(patterns["DASHES"]["expression"],r'-', cleaned_text)
    #Replace '\'  with '\\'
    cleaned_text = re.sub(patterns["BACKSLASH"]["expression"],r'\\\\', cleaned_text)
    #Replace for exemple ',mot'  with  ', mot '
    cleaned_text = re.sub(patterns["COMA_NUMBERS"]["expression"],r'\1.\3', cleaned_text)
    #Replace for example 'a=  b' by 'a=b'
    cleaned_text = re.sub(patterns["MATH_OP_EXTRA_SPACES"]["expression"],r'\1\2\3', cleaned_text)
    # For SI units like '1.5 m' which will be changed to '1.5m' 
    cleaned_text = re.sub(patterns["SI_UNITS_SPACE"]["expression"],r'\1\2', cleaned_text)
    #Replace again a consecutive repetition of '\n' character with white space
    cleaned_text = re.sub(patterns["SPACES"]["expression"],r' ', cleaned_text)
    #Replace for example '( some_expression )' with '(some_expression )'
    cleaned_text = re.sub(patterns["BRACKETS_SPACES"]["expression"],r'\1\2\3', cleaned_text)
    #Replace for exemple 'mot ,' with 'mot,'
    cleaned_text = re.sub(patterns["WORD_SPACES_COMA-DOT"]["expression"],r'\1\2', cleaned_text)
    #Replace for exemple ',mot'  with  ', mot '
    cleaned_text = re.sub(patterns["COMA_WORD"]["expression"],r'\1 \2', cleaned_text) 
    #Replace for exemple "word1:  word 2" by "word1 : word 2"
    cleaned_text = re.sub(patterns["WORD_COLON"]["expression"],r'\1 \2 ', cleaned_text) 
    # Replace . § with .
    cleaned_text = re.sub(r'\.\s§',r'.', cleaned_text) 

    return cleaned_text

def get_init(user: str, host: str, database: str, password: str, name : str, regex : str):
    """
    Get all cleaned (only HTML) text Labdocs
    """
    typer.secho(f'-- Get all cleaned text Labdocs', fg=typer.colors.BRIGHT_BLUE)

    # query = f' SELECT  t2.labdoc_data, t1.id_labdoc, t1.id_report  FROM labdoc t1 LEFT JOIN labdoc t2 ON t2.id_labdoc = t1.id_ld_origin WHERE t1.type_labdoc = "text" AND t1.id_report IS NOT NULL AND t1.id_ld_origin IS NOT NULL AND t2.labdoc_data IS NOT NULL AND t2.labdoc_data != " " LIMIT 10 '

    # query  = f' SELECT t1.id_labdoc, t2.labdoc_data FROM labdoc t1 LEFT JOIN labdoc t2 ON t2.id_labdoc = t1.id_ld_origin WHERE t1.deleted IS NULL AND t1.id_ld_origin IS NOT NULL AND t1.type_labdoc = "text" AND t1.id_report IS NOT NULL AND t1.name != "" AND t2.labdoc_data != "" AND t2.name IS NOT NULL group by t1.id_report;'

    # query  = f' SELECT DISTINCT t1.labdoc_data, t1.id_labdoc, t1.id_report  FROM labdoc t1  WHERE t1.deleted IS NULL AND  t1.labdoc_data != ""  AND t1.id_ld_origin IS NOT NULL AND t1.type_labdoc = "text" AND t1.id_report IS NOT NULL AND t1.name != ""  AND t1.id_report in  (SELECT DISTINCT id_report  from trace where id_mission IS NOT NULL  and id_report IS NOT NULL) LIMIT 10;'
    # # #ORDER BY RAND() 

    # query = """
    #     SELECT   l.labdoc_data, l.id_labdoc, l.id_report, t.id_mission from labdoc l JOIN trace t ON l.id_labdoc = t.id_labdoc 
    #     where  l.type_labdoc = "text" 
    #     AND l.id_report IS NOT NULL  
    #     AND deleted IS NULL AND l.id_ld_origin IS NOT NULL 
    #     AND l.name != ""  
    #     AND  l.labdoc_data != "" 
    #     GROUP by t.id_mission
    #     """
    query = """
            SELECT  labdoc_data, id_labdoc, id_report, id_mission 
            FROM labdoc 
            JOIN report_part 
            USING(id_report_part)
            WHERE type_labdoc = 'text' 
            AND labdoc_data != "" 
            AND id_report IS NOT NULL 
            AND deleted IS NULL
            GROUP BY id_report 
            """
    table = execute_query(user, host, database, password, query)
    pbar = tqdm(total=len(table),ascii=' >=')

    # Extract data from table
    data = []

    for row in table:
        text_init = clean_text(text=row[0],regex = regex)
        pbar.update(n=1)
        if text_init != '':
            data_row = {"text":str,"meta":{"id_labdoc":int,"id_report":int,"id_mission":int}}
            #data_line["text"] = text_init
            data_row["text"] =  text_init
            data_row["meta"]["id_labdoc"] = row[1]
            data_row["meta"]["id_report"] = row[2]
            data_row["meta"]["id_mission"] = row[3]
        data.append(data_row)


    # Save data in a JSONL file
    data_to_jsonl(data, 'source', name)

if __name__  == '__main__':
    typer.run(get_init)

