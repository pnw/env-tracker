import os
from pathlib import Path


class config(object):
    """
    Just a dumb object to house the app config.
    Makes things easier to mock instead of global variables.
    """
    ET_HOME = Path(os.environ.get('ET_HOME', str(Path.home() / '.et'))) or '.et'
    PARENT_SYMLINK_NAME = os.environ.get('ET_PARENT_SYMLINK_NAME', '.source') or '.source'

    def __init__(self):
        raise RuntimeError('Do not init config object')
