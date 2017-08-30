from pathlib import Path

from git import Repo, InvalidGitRepositoryError

from config import PARENT_SYMLINK_NAME, ET_HOME
from exceptions import InETHome, NotInProject, MissingChild


def path_is_child_repo(path: Path) -> bool:
    return path / PARENT_SYMLINK_NAME


def find_child_dir(parent_dir: Path) -> Path:
    """
    Browse the ET_HOME directory to find the directory that tracks the parent dir
    """
    if parent_dir == ET_HOME or ET_HOME in parent_dir.parents:
        raise Exception(f'Cannot run this from within {ET_HOME}')

    for child_dir in ET_HOME.iterdir():
        if child_dir.name in ['.git']:
            # skip special directories
            continue

        parent_path = (child_dir / PARENT_SYMLINK_NAME).resolve()
        if parent_dir == parent_path:
            return child_dir

    # User needs to run `et init` on the parent directory.
    raise MissingChild('Could not find an associated project for the current directory')


class Project(object):
    def __init__(self, parent_dir, child_dir):
        self.parent_dir = parent_dir
        self.child_dir = child_dir

    def child_file_exists(self, fpath: Path) -> bool:
        return (self.child_dir / fpath).exists()

    def parent_file_exists(self, fpath: Path) -> bool:
        return (self.parent_dir / fpath).exists()

    def corresponding_child_path(self, fpath: Path) -> bool:
        try:
            relative_to_parent  = fpath.resolve().relative_to(self.parent_dir)
        except VaueError:
            raise Exception(f'"{fpath}" not found in "{self.parent_dir}"')
        return self.child_dir / relative_to_parent

    def relative_to_parent(self, fpath: Path) -> Path:
        return fpath.resolve().relative_to(self.parent_dir)

    def relative_to_child(self, fpath: Path) -> Path:
        return fpath.resolve().relative_to(self.child_dir)


def init_project_from_path(pth: Path) -> Project:
    try:
        repo = Repo(pth, search_parent_directories=True)
    except InvalidGitRepositoryError:
        raise

    working_repo_dir = Path(repo.working_dir)

    if ET_HOME in working_repo_dir.parents or pth == ET_HOME:
        # running a command from the ET_HOME directory. Not allowed
        raise InETHome(f'Cannot use et from within {ET_HOME}')

    child_dir = find_child_dir(working_repo_dir)

    return Project(working_repo_dir, child_dir)
