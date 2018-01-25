import os
from pathlib import Path

ET_HOME = Path(os.environ.get('ET_HOME', str(Path.home() / '.et'))) or '.et'

PARENT_SYMLINK_NAME = os.environ.get('ET_PARENT_SYMLINK_NAME', '.source') or '.source'
