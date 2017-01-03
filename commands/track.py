from pathlib import Path

from logger import log
import os
from config import intuit_project_from_path

def track (filepath, *opts):
    """
    1. move the file to the et directory
    2. track the file in the et repo
    3. commit the file in the et repo
    4. symlink the file back to the original location
    5. possibly gitignore the symlinked file in the repo, or at least post a warning that et doesn't do that for the user
    :param args:
    :return:
    """
    file_path = Path(filepath).resolve()

    if not file_path.exists():
        raise Exception('Path does not exist')

    if not file_path.is_file():
        raise Exception('Path provided is not a file')

    if file_path.is_symlink():
        raise Exception('File is already symlinked')

    # TODO: raise exception if the file is being tracked by the source repo - otherwise moving it to the parallel dir doesn't make sense

    project = intuit_project_from_path(file_path)

    try:
        relative_path = file_path.relative_to(project.source_dir)
    except ValueError:
        # TODO: make this error clearer
        raise Exception('May not track files from the follower directory.')

    destination_path = project.follower_dir / relative_path

    if destination_path.exists():
        raise Exception('Something else already exists at: {}'.format(destination_path))

    file_path.replace(destination_path)
    file_path.symlink_to(destination_path)
    # TODO: git add and commit the new file to the follower repo
