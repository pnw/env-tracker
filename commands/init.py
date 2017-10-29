from pathlib import Path
from git import Repo, InvalidGitRepositoryError
from config import ET_HOME, PARENT_SYMLINK_NAME
from utils import find_child_dir

# TODO: make this only accept a Path instance - need to use
def init(parent_dir: [str, Path] = None, project_name: str = None) -> None:
    """
    usage: `et init [parent_dir] [project_name]`
    TODO: allow the user to specify the parent_dir to the project instead of relying on the current directory

    Initialize a project
    1. Detects the current repo
    2. Grab the name of the current repo and create a parallel git repo in the ER_DIR

    :param parent_dir: Path to use as the parent project
    :param project_name: Name of the directory to store the child dir in ET_HOME directory
    """
    # handled by click
    if parent_dir is None:
        # TODO: test
        # Use current directory
        parent_dir = Path().resolve()

    # handled by click
    elif isinstance(parent_dir, str):
        # TODO: test
        # Use specified directory
        parent_dir = Path(parent_dir).resolve()
    else:
        # parent_dir is instance of Path
        parent_dir = parent_dir.resolve()

    # Source must be a directory. Doesn't make sense otherwise
    # handled by click
    if not parent_dir.is_dir():
        # TODO: test
        raise Exception(f'{parent_dir} is not a valid directory')

    if not project_name:
        project_name = parent_dir.name

    child_path = Path(ET_HOME) / project_name

    if child_path.exists():
        # TODO: make this more fault-tolerant by inpecting the child parent_dir
        # if the child parent_dir is already linked to the current project, then we don't need to fail
        raise Exception('Follower directory already exists')

    # make sure we aren't already tracking
    try:
        current_child_dir = find_child_dir(parent_dir)
    except Exception:
        pass
    else:
        raise Exception(f'This repo is already linked to {current_child_dir}')

    # Initialize the child dir and repo
    child_path.mkdir(parents=True)
    Repo.init(child_path)

    # create a symlink file that points to the parent directory
    to_parent_symlink = child_path / PARENT_SYMLINK_NAME
    to_parent_symlink.symlink_to(parent_dir)

    # TODO: register a post-commit hook to automatically commit changes in the child directory

    print('Success! New env-tracker repository initialized at {0}'.format(child_path))
