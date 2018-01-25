from pathlib import Path

from config import config

def patch_et_home(location: Path):
    """
    WARNING: This should only be used in tests

    Override the config settings to point ET_HOME to a new value

    :param location: path to set the ET_HOME config value to
    """
    config.ET_HOME = location
