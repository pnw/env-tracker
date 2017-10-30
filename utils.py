from pathlib import Path

import click
from git import Repo, InvalidGitRepositoryError

from config import PARENT_SYMLINK_NAME, ET_HOME
from exceptions import MissingChild


class PairedProject(object):
    """
    Represents a pair of repositories that are linked together
    """

    def __init__(self, parent_dir: Path, child_dir: Path, working_from_parent: bool):
        """
        :param parent_dir: the project repo
        :param child_dir: the et repo where we keep tracked files
        """
        self.parent_dir = parent_dir
        self.child_dir = child_dir
        self.working_from_parent = working_from_parent

    @classmethod
    def from_path(cls, input_path: Path):
        """
        Identify a ProjectPair given a path.
        An error will be raised if the input_path is not in a valid
         project directory
        """
        try:
            repo = Repo(input_path, search_parent_directories=True)
        except InvalidGitRepositoryError:
            raise

        working_repo = Path(repo.working_dir)

        if ET_HOME in working_repo.parents:
            parent_dir = (working_repo / PARENT_SYMLINK_NAME).resolve()
            return cls(parent_dir=parent_dir, child_dir=working_repo, working_from_parent=False)
        else:
            child_dir = find_child_dir(working_repo)
            return cls(parent_dir=working_repo, child_dir=child_dir, working_from_parent=True)

    @property
    def parent_repo(self):
        return Repo(str(self.parent_dir))

    @property
    def child_repo(self):
        return Repo(str(self.child_dir))


class PairedPath(object):
    """
    Represents a Path that exists under one or both of the
    projects in a project pair.
    """

    def __init__(self, project: PairedProject, original_path: Path):
        self.project = project
        self.original_path = original_path.absolute()
        self.relative_path = get_relative_path(project, self.original_path)

    @classmethod
    def from_path(cls, input_path: Path):
        """
        Constructor method that creates a ProjectPair instance from the path too.
        """
        return cls(PairedProject.from_path(input_path), original_path=input_path)

    @property
    def working_from_parent(self):
        """
        :return: Whether not the original referenced file is in the parent dir
        """
        return self.project.working_from_parent

    @property
    def child_path(self) -> Path:
        return self.project.child_dir / self.relative_path

    @property
    def parent_path(self) -> Path:
        return self.project.parent_dir / self.relative_path

    @property
    def is_linked(self):
        """
        True if the path matches the pattern for a tracked file.
        """
        # import ipdb; ipdb.set_trace()
        return self.parent_path.is_symlink() \
               and (not self.child_path.is_symlink()) \
               and self.child_path.samefile(self.parent_path)

    def link(self):
        # move the file over to the child dir
        self.parent_path.replace(self.child_path)

        # symlink the file back to its original location
        self.parent_path.symlink_to(self.child_path)

    def unlink(self):
        # This should always be a symlink, so no need to handle this being a dir instead
        # remove the symlink
        self.parent_path.unlink()

        # move the file back to its original location
        self.child_path.replace(self.parent_path)


def get_relative_path(project: PairedProject, input_path: Path) -> Path:
    """
    Finds the relative path for a path under either of the project dirs
    """
    abs_path = input_path.absolute()
    try:
        return abs_path.relative_to(project.parent_dir)
    except ValueError:
        pass

    try:
        return abs_path.relative_to(project.child_dir)
    except ValueError:
        pass

    raise ValueError(f'"{input_path}" not found in "{project.parent_dir}" '
                     f'or "{project.child_dir}"')


def find_child_dir(parent_dir: Path) -> Path:
    """
    Browse the ET_HOME directory to find the directory
     that tracks the parent dir
    """
    for child_dir in ET_HOME.iterdir():
        parent_path = (child_dir / PARENT_SYMLINK_NAME).resolve()
        if parent_dir == parent_path:
            return child_dir

    # User needs to run `et init` on the parent directory.
    raise MissingChild('Could not find an associated project '
                       'for the current directory')

def get_current_project():
    try:
        return PairedProject.from_path(Path('.'))
    except InvalidGitRepositoryError:
        raise click.BadParameter('Not in a git repository')
    except MissingChild as e:
        raise click.BadParameter(e)
