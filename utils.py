from pathlib import Path

import click
from git import Repo, InvalidGitRepositoryError, Git

from config import config
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
    def from_path(cls, input_path: Path) -> 'PairedProject':
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

        if config.ET_HOME in working_repo.parents:
            # We are in a child directory
            parent_dir = (working_repo / config.PARENT_SYMLINK_NAME).resolve()
            return cls(parent_dir=parent_dir, child_dir=working_repo, working_from_parent=False)
        else:
            # We are in a parent directory
            child_dir = find_child_dir(working_repo)
            return cls(parent_dir=working_repo, child_dir=child_dir, working_from_parent=True)

    @property
    def parent_repo(self):
        return Repo(str(self.parent_dir))

    @property
    def child_repo(self):
        return Repo(str(self.child_dir))


class PairedObject(object):
    """
    Represents a filesystem object (file, directory, other?)
    whose path is under a ProjectPair.
    """

    def __init__(self, project: PairedProject, relative_path: Path):
        self.project = project
        self.relative_path = relative_path

    @classmethod
    def from_path(cls, input_path: Path) -> 'PairedObject':
        """
        Constructor method that creates a ProjectPair instance from the path too.
        """
        project = PairedProject.from_path(input_path)
        relative_path = get_relative_path(project, input_path.absolute())

        return cls(project, relative_path=relative_path)

    @property
    def working_from_parent(self) -> bool:
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
    def is_linked(self) -> bool:
        """
        A path is considered linked if the path
        meets the following qualifications:

            - child path exists
            - child path is not a symlink
            - parent path exists
            - parent path is a symlink to the child
        """
        return self.parent_path.is_symlink() \
               and (not self.child_path.is_symlink()) \
               and self.child_path.samefile(self.parent_path)

    def link(self):
        """
        1. Moves the file/directory from the parent dir into
        the same relative location in the child dir.
        2. Symlink the file/directory back to its original location
        """
        self.parent_path.replace(self.child_path)
        self.parent_path.symlink_to(self.child_path)

    def unlink(self):
        """
        Completely reverts changes made by PairedPath.link.
        """
        # No special case needed for file vs dir types, since this is always a symlink
        self.parent_path.unlink()
        self.child_path.replace(self.parent_path)


def get_relative_path(project: PairedProject, input_path: Path) -> Path:
    """
    Finds the relative path for a path under either of the project dirs

    :param project: A PairedProject instance
    :param input_path: A path that should be under one of the projects two directories.
    :raises ValueError: if input_path is not found under one of the project directories
    :return:
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
     that symlinks to the parent dir
    """
    for child_dir in config.ET_HOME.iterdir():
        parent_path = (child_dir / config.PARENT_SYMLINK_NAME).resolve()
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


class PathType(click.Path):
    """
    Click argument parser for returning filepath locations as Path objects
    """

    def convert(self, value, param, ctx):
        return Path(super().convert(value, param, ctx))


# TODO: I forget what I was going to use this for... should this be a method on PairedObject?
def file_is_git_tracked(repo: Repo, file: Path) -> bool:
    """
    :param repo: any git Repo instance
    :param file: path must be relative to the repo
    :return: Whether git is tracking the file in question
    """
    # TODO: is there a more canonical way of doing this?
    # Git knows about this file
    return bool(Git(repo.working_dir).ls_files(file))
