from pathlib import Path
from git import Repo, InvalidGitRepositoryError

from config import ET_HOME
from config import PARENT_SYMLINK_NAME
from exceptions import InETHome
from utils import find_child_dir, init_project_from_path, path_in_et_home


def track(filepath: [str, Path]):
    """
    1. move the file to the et directory
    2. track the file in the et repo
    3. commit the file in the et repo
    4. symlink the file back to the original location
    5. possibly gitignore the symlinked file in the repo, or at least post a warning that et doesn't do that for the user
    :param args:
    :return:
    """
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError('Path does not exist')

    if file_path.is_symlink():
        raise Exception('File is already symlinked')

    if path_in_et_home(file_path):
        raise InETHome(f'Cannot track files from within {ET_HOME}')

    project = init_project_from_path(file_path)

    parent_dir = project.parent_dir
    child_dir = project.child_dir

    try:
        relative_path = file_path.resolve().relative_to(parent_dir)
    except ValueError:
        raise Exception(f'May only track files under {parent_dir}')

    destination_path = child_dir / relative_path

    if destination_path.exists():
        raise Exception('Something else already exists at: {}'.format(destination_path))

    # move the file to the child dir
    file_path.replace(destination_path)
    # symlink the file back to its original location
    file_path.symlink_to(destination_path)
    # TODO: git add and commit the new file to the child repo
