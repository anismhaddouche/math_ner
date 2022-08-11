from spacy.cli.project.run import project_run
#from spacy.cli.project.assets import project_assets
from pathlib import Path


def run_project():
    root = Path(__file__).parent
    project_run(root, "get_labdocs", capture=False)
    project_run(root, "train_ner", capture=False)
    
run_project()
