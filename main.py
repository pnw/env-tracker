from pathlib import Path

import click
from git import Repo
from git.exc import InvalidGitRepositoryError

from config import ET_HOME, PARENT_SYMLINK_NAME


@click.group()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose messaging')
@click.pass_context
def et(ctx, verbose):
    click.echo('Running an et command!!')
    ctx.obj = {}
    ctx.obj['verbose'] = verbose
    click.echo(f'Verbosity {ctx.obj["verbose"]}')


def convert_to_path(ctx, param, value: str) -> Path:
    return Path(value)


@et.command('init', short_help='Initialize a new Env Tracker repository')
@click.argument('directory', default='.',
                type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
                callback=convert_to_path)
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
            raise click.BadParameter(f'{child_path} already exists and links to: {to_parent_symlink.resolve()}',
                                     param_hint=['name'])
        else:
            raise click.BadParameter(f'{child_path} already exists', param_hint=['name'])
    repo = Repo.init(child_path)
    to_parent_symlink.symlink_to(parent_path)

    repo.index.add([PARENT_SYMLINK_NAME])
    repo.index.commit('Link project to parent directory')

    click.echo(f'Installed new project "{name}", linking {child_path} -> {parent_path}')


@et.command()
def track():
    click.echo('Running track command')


@et.command()
def untrack():
    click.echo('Running untrack command')
