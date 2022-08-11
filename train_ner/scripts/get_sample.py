import typer 
from utility import *
import re 
import random 
from pathlib import Path
import srsly

def get_sample(input_file: str, output_file: str, sample_size: int, patterns_file : Path):
    """
    Get a sample of Labdocs that contains  the regex expressions in the patterns_file
    """
    
    #patterns = {"LATEX_MATH":  r"[$]{1,2}(.*?)[$]{1,2}", "TEXT_MATH": r"(\s\S+=\S+\s)","TABLE":r'¥(.*?)¥'}

    patterns = srsly.read_json(patterns_file)
    # = {"latex_equation":  r"[$]{1,2}(.*?)[$]{1,2}", "text_equation": r"(\s{0,}\S+=\S+\s{0,})"}
    typer.secho(f'-- Get a sample of {sample_size} Labdocs  with equations from {input_file}',fg=typer.colors.BRIGHT_BLUE)
    # Read a Jsonl file
    data = []
    with jsonlines.open(input_file) as f:
        for line in f.iter():
            if line['text'] != '' and line['text'] != ' ':
                for label, regex in patterns.items():
                    found = re.search(regex, line['text'])
                    if found is not None:
                        data.append(line)
    sample = random.sample(data, sample_size)
    # Write to a Jsonl file
    with jsonlines.open(output_file, mode='w') as f:
        for line in sample:
            f.write(line)
if __name__ == "__main__":
    typer.run(get_sample)

# get_sample('/Users/anis/test_labnbook/math_ner/get_annotate_convert_assets/source/labdoc_init.jsonl','/Users/anis/test_labnbook/math_ner/get_annotate_convert_assets/source/labdoc_sample.jsonl', sample_size = 20, patterns_file = "/Users/anis/test_labnbook/math_ner/get_annotate_convert_assets/source/regex_ner.json")
