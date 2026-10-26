"""The former dropdown picker is replaced by the shared selection dialog."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('problem-dialog.py')),run_name='__main__')
