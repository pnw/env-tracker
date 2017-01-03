import os
from pathlib import Path

ET_HOME = Path(os.environ.get('ET_HOME', str(Path.home() / '.et')))

FOLLOWER_SYMLINK_NAME = os.environ.get('ET_FOLLOWER_SYMLINK_NAME', '.tracking')
SOURCE_SYMLINK_NAME = os.environ.get('ET_SOURCE_SYMLINK_NAME', '.source')
