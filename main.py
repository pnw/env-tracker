from pathlib import Path

import click
from git import Repo
from git.exc import InvalidGitRepositoryError

from logger import logger
from config import config
from utils import PairedObject, PairedProject, get_current_project, PathType


@click.group()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose messaging')
@click.pass_context
def et(ctx: click.core.Context, verbose: bool):
    """
    Primary top-level group command.
    Calling directly with no parameters will display help.
    """
    ctx.obj = {}
    ctx.obj['verbose'] = verbose


@et.command('init', short_help='Initialize a new Env Tracker repository')
@click.argument('directory', default='.',
                type=PathType(exists=True, file_okay=False, dir_okay=True, resolve_path=True, allow_dash=False))
@click.option('-n', '--name', type=click.STRING)
def cmd_init(directory: Path, name: str):
    """
    Create an empty Git repository that points to an existing repository
    """
    try:
        existing_project = PairedProject.from_path(directory)
    except Exception:
        logger.debug('No existing project found - continuing')
    else:
        raise click.BadParameter(
            f'Conflict: specified directory is already linked to {str(existing_project.child_dir)}',
            param_hint='DIRECTORY')

    ## Validate parameters and set defaults
    try:
        repo = Repo(directory, search_parent_directories=False)
    except InvalidGitRepositoryError:
        try:
            # Check if the directory is a subdir of a git repo and suggest that
            repo = Repo(directory, search_parent_directories=True)
        except InvalidGitRepositoryError:
            raise click.BadParameter('Not a git repository.', param_hint=['directory'])
        else:
            raise click.BadParameter(f'Not a git repository. Did you mean this?\n\n\t{repo.working_dir}',
                                     param_hint=['directory'])

    parent_path = Path(repo.working_dir)
    if name:
        # names must not contain OS path delimiters
        if Path(name).name != name:
            raise click.BadParameter('Must not contain path delimiter, e.g. "/" or "\\"', param_hint=['name'])
    else:
        name = parent_path.name
    child_path: Path = Path(config.ET_HOME) / name
    to_parent_symlink: Path = child_path / config.PARENT_SYMLINK_NAME

    ## Attempt to create the child directory
    try:
        child_path.mkdir(parents=True)
    except FileExistsError:
        if to_parent_symlink.exists():
            raise click.BadParameter(
                f'Path "{child_path}" already exists and links to: "{to_parent_symlink.resolve()}"',
                param_hint=['name'])
        else:
            raise click.BadParameter(f'Path "{child_path}" already exists', param_hint=['name'])

    ## Initialize the child repo
    repo = Repo.init(child_path)
    to_parent_symlink.symlink_to(parent_path)

    repo.index.add([config.PARENT_SYMLINK_NAME])
    repo.index.commit('Link project to parent directory')

    click.echo(f'Installed new project "{name}", linking "{child_path}" -> "{parent_path}"')


@et.command('link', short_help='Link a file or directory')
@click.argument('file', type=PathType(exists=True, file_okay=True, dir_okay=True, allow_dash=False, writable=True,
                                      readable=True, resolve_path=False))
def cmd_link(file: Path):
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

    obj_pair = PairedObject.from_path(file)
    if obj_pair.is_linked:
        raise click.BadParameter(f'Path "{obj_pair.relative_path}" is already linked')

    if obj_pair.parent_path.is_symlink():
        raise click.BadParameter(f'Path "{file}" is already a symlink', param_hint=['file'])

    if not obj_pair.working_from_parent:
        raise click.BadParameter(f'Path "{file}" not found under "{obj_pair.project.parent_dir}"',
                                 param_hint=['file'])

    if obj_pair.child_path.exists():
        raise click.BadParameter(f'Destination path "{obj_pair.child_path}" already exists', param_hint=['file'])

    obj_pair.link()

    # commit the new file
    child_repo = obj_pair.project.child_repo
    child_repo.index.add([str(obj_pair.relative_path)])
    child_repo.index.commit(f'Initialize tracking for "{obj_pair.relative_path}"')


@et.command('unlink', short_help='Stop tracking a file or directory')
@click.argument('file', type=PathType(exists=True, file_okay=True, dir_okay=True, allow_dash=False, writable=True,
                                      readable=True, resolve_path=False))
def cmd_unlink(file: Path):
    """
    Unlinks a tracked file by reverting the changes made by the `link` command

    TODO: add an `--all` option to unlink all objects
    """
    ## Validate parameters and set defaults
    obj_pair = PairedObject.from_path(file)

    if not obj_pair.is_linked:
        raise click.BadParameter('File is not linked', param_hint=['file'])

    ## Unlink files
    obj_pair.unlink()

    ## Commit changes
    child_repo = obj_pair.project.child_repo
    child_repo.index.remove([str(obj_pair.relative_path)])
    child_repo.index.commit(f'Stop tracking for "{obj_pair.relative_path}"')


@et.command('status', short_help='`git status` on the linked repository')
def cmd_status():
    proj = get_current_project()
    g = proj.child_repo.git
    click.echo(click.style(f'Showing git status for "{proj.child_dir}"', fg='red'))
    click.echo()
    click.echo(g.status())


@et.command('other', short_help='Output the linked repository directory')
def cmd_other():
    """
    Writes the linked directory of the current location to stdout

    Example usage:

        cd `et other` - changes directory back and forth between linked repositories
    """
    proj = get_current_project()

    other_dir = proj.child_dir if proj.working_from_parent else proj.parent_dir

    click.echo(other_dir)


@et.command('commit', short_help='Commit all changes to the linked directory')
@click.option('-m', '--message', type=click.STRING, default='Saving changes')
def cmd_commit(message):
    """
    Commits all changes to the linked repository using `git add -u`
    """
    proj = get_current_project()
    proj.child_repo.git.add(update=True)  # git add -u
    proj.child_repo.index.commit(message)
