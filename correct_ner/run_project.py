from spacy.cli.project.run import project_run
from spacy.cli.project.assets import project_assets
from pathlib import Path
import subprocess
import sys




def run_correct_dev():
    root = Path(__file__).parent
    project_run(root,"correct_dev", capture=False)

def run_correct_train():
    root = Path(__file__).parent
    project_run(root,"correct_train", capture=False)


def run_correct_ner():
    root = Path(__file__).parent
    #
    project_run(root,"correct_ner", capture=False)


def run_get_devtrain_from_db():
    root = Path(__file__).parent
    project_run(root,"get_devtrain_from_db", capture=False)

# def run_final_ner():
#     root = Path(__file__).parent
#     project_run(root,"final_ner", capture=False)

#run_correct_train()
#run_correct_dev()

#run_get_devtrain_from_db()
run_correct_ner()
# run_final_ner()

