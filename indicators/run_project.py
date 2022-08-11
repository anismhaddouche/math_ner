
from spacy.cli.project.run import project_run
#from spacy.cli.project.assets import project_assets
from pathlib import Path
import typer 

from datetime import datetime
# do your work here

def run_project():
    root = Path(__file__).parent
    start_time = datetime.now()
    # project_run(root, "extract_labdoc_text_versions", capture=False)
    project_run(root,"compute_contributions_matrices",capture=False)
    end_time = datetime.now()
    typer.secho(f"Duration: {end_time - start_time}",fg=typer.colors.GREEN)
run_project()


