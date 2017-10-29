from pathlib import Path

import click
from git import Repo, Git
from git.exc import InvalidGitRepositoryError

from config import ET_HOME, PARENT_SYMLINK_NAME
from utils import ProjectPair, find_child_dir, File


@click.group()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose messaging')
@click.pass_context
def et(ctx, verbose):
    ctx.obj = {}
    ctx.obj['verbose'] = verbose


class PathType(click.Path):
    def convert(self, value, param, ctx):
        return Path(super().convert(value, param, ctx))


@et.command('init', short_help='Initialize a new Env Tracker repository')
@click.argument('directory', default='.',
                type=PathType(exists=True, file_okay=False, dir_okay=True, resolve_path=True, allow_dash=False))
@click.option('-n', '--name', type=click.STRING)
@click.pass_context
def cmd_init(ctx: click.core.Context, directory: Path, name: str):
    """
    Create an empty Git repository that points to an existing repository
    """
    try:
        repo = Repo(directory, search_parent_directories=True)
    except InvalidGitRepositoryError:
        raise click.BadParameter('Not a git repository (or any of the parent directories)', param_hint=['directory'])

    parent_path = Path(repo.working_dir)
    if not name:
        name = parent_path.name
    child_path = Path(ET_HOME) / name
    to_parent_symlink = child_path / PARENT_SYMLINK_NAME

    try:
        child_path.mkdir(parents=True)
    except FileExistsError:
        if to_parent_symlink.exists():
            raise click.BadParameter(f'Path "{child_path}" already exists and links to: "{to_parent_symlink.resolve()}"',
                                     param_hint=['name'])
        else:
            raise click.BadParameter(f'Path "{child_path}" already exists', param_hint=['name'])
    repo = Repo.init(child_path)
    to_parent_symlink.symlink_to(parent_path)

    repo.index.add([PARENT_SYMLINK_NAME])
    repo.index.commit('Link project to parent directory')

    click.echo(f'Installed new project "{name}", linking "{child_path}" -> "{parent_path}"')


def file_is_git_tracked(repo: Repo, file: Path) -> bool:
    """
    :param repo:
    :param file: path must be relative to the repo
    :return: Whether git is tracking the file in question
    """
    # Git knows about this file
    return bool(Git(repo.working_dir).ls_files(file))


@et.command('track', short_help='Track a file or directory')
@click.argument('file', type=PathType(exists=True, file_okay=True, dir_okay=True, allow_dash=False, writable=True,
                                      readable=True, resolve_path=False))
def cmd_track(file: Path):
    """
    Tracks a file in the parent repo.

    Moves the specified file to the child repository and symlinks the file back to
    its original location.

    Validations:
    - path exists
    - path exists under the parent dir
    - path does not exist under the child dir
    - parent path is not a symlink
    """
    # We check for symlink here because we resolve the file path to init the project
    if file.is_symlink():
        raise click.BadParameter(f'Path "{file}" is already a symlink', param_hint=['file'])

    f_pair = File.from_path(file)
    if not f_pair.working_from_parent:
        raise click.BadParameter(f'Path "{file.resolve()}" not found under "{f_pair.project.parent_dir}"', param_hint=['file'])

    if f_pair.child_path.exists():
        raise click.BadParameter(f'Destination path "{f_pair.child_path}" already exists', param_hint=['file'])

    # move the file over to the child dir
    f_pair.parent_path.replace(f_pair.child_path)

    # symlink the file back to its original location
    f_pair.parent_path.symlink_to(f_pair.child_path)

    # commit the new file
    child_repo = f_pair.project.child_repo
    child_repo.index.add([str(f_pair.relative_path)])
    import ipdb; ipdb.set_trace()
    child_repo.index.commit(f'Initialize tracking for "{f_pair.relative_path}"')


@et.command()
def untrack():
    click.echo('Running untrack command')
