"""Current editor workflow supersedes earlier publication/autosave contracts."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name("publication-workflow.py")),run_name="__main__")
