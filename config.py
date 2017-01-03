import os
from pathlib import Path

ET_HOME = os.environ.get('ET_HOME', os.path.join(os.path.expanduser('~'), '.et'))

ET_CONFIG_LOCATION = os.environ.get('ET_CONFIG_LOCATION', os.path.join(ET_HOME, '.etconfig'))

TO_FOLLOWER_SYMLINK_NAME = os.environ.get('ET_TO_FOLLOWER_SYMLINK_NAME', '.et')
TO_SOURCE_SYMLINK_NAME = os.environ.get('ET_TO_SOURCE_SYMLINK_NAME', '.source')

ET_ROOT_PATH = Path(ET_HOME)
ET_CONFIG_PATH = Path(ET_CONFIG_LOCATION)
