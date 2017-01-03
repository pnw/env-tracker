from pathlib import Path
from git import Repo, InvalidGitRepositoryError
from logger import log
from config import ET_FOLLOWER_ROOT_DIR, ET_SYMLINK_NAME


def init(path: str, project_name: str = ''):
    """
    usage: `et init path [project_name]`
    TODO: allow the user to specify the path to the project instead of relying on the current directory

    Initialize a project
    1. Detects the current repo
    2. Grab the name of the current repo and create a parallel git repo in the ER_DIR
    """
    try:
        repo = Repo(path=path, search_parent_directories=True)
    except InvalidGitRepositoryError as e:
        log.debug('TODO: Give better error when we arent in a repo')
        raise

    source_path = Path(repo.working_dir)

    if not project_name:
        project_name = source_path.name

    follower_path = Path(ET_FOLLOWER_ROOT_DIR) / project_name
    sympath = source_path / ET_SYMLINK_NAME

    # ETAFTP, I know, but this prevents me from having to rollback in the event of errors
    if follower_path.exists():
        # TODO: make this more fault-tolerant by inpecting the follower path
        # if the follower path is already linked to the current project, then we don't need to fail
        raise Exception('Follower directory already exists')

    if sympath.exists():
        # TODO: make this more fault tolerant by inspecting the symlink path
        raise Exception('This repo is already linked to a follower directory')

    follower_path.mkdir()
    sympath.symlink_to(follower_path)

    Repo.init(follower_path)

    print('Success! New env-tracker repository initialized at {0}'.format(follower_path))
