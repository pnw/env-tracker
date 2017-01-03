from pathlib import Path
from git import Repo, InvalidGitRepositoryError

from config import FOLLOWER_SYMLINK_NAME, SOURCE_SYMLINK_NAME


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

    try:
        repo = Repo(file_path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        raise Exception('Not in a project')

    source_dir = Path(repo.working_dir)
    follower_dir = (source_dir / FOLLOWER_SYMLINK_NAME).resolve()

    if (source_dir / SOURCE_SYMLINK_NAME).exists():
        raise Exception('You may not track files from the follower directory')

    if not (source_dir / FOLLOWER_SYMLINK_NAME).exists():
        raise Exception('Cannot find reference to a follower directory')

    if (follower_dir / SOURCE_SYMLINK_NAME).resolve() != source_dir:
        # TODO: add a "doctor" command to fix symlinks between repos, `et doctor source_dir follower_dir`
        raise Exception('Project misconfigured - the follower directory is tracking a different project')

    try:
        relative_path = file_path.resolve().relative_to(source_dir)
    except ValueError:
        raise Exception('May only track files in the source directory')

    destination_path = follower_dir / relative_path

    if destination_path.exists():
        raise Exception('Something else already exists at: {}'.format(destination_path))

    file_path.replace(destination_path)
    file_path.symlink_to(destination_path)
    # TODO: git add and commit the new file to the follower repo
