from pathlib import Path
from git import Repo, InvalidGitRepositoryError
from config import ET_HOME, TO_FOLLOWER_SYMLINK_NAME, TO_SOURCE_SYMLINK_NAME


def init(path: str, project_name: str = ''):
    """
    usage: `et init path [project_name]`
    TODO: allow the user to specify the path to the project instead of relying on the current directory

    Initialize a project
    1. Detects the current repo
    2. Grab the name of the current repo and create a parallel git repo in the ER_DIR
    """
    ## TODO: if no path is provided, then we can crawl up the tree to the nearest git repo to
    try:
        repo = Repo(path=path)
    except InvalidGitRepositoryError:
        raise Exception('Provided path is not a git repository')

    source_path = Path(repo.working_dir)

    if not project_name:
        project_name = source_path.name

    follower_path = Path(ET_HOME) / project_name
    to_follower_symlink = source_path / TO_FOLLOWER_SYMLINK_NAME
    to_source_symlink = follower_path / TO_SOURCE_SYMLINK_NAME

    if follower_path.exists():
        # TODO: make this more fault-tolerant by inpecting the follower path
        # if the follower path is already linked to the current project, then we don't need to fail
        raise Exception('Follower directory already exists')

    if to_follower_symlink.exists():
        # TODO: make this more fault tolerant by inspecting the symlink path
        raise Exception('This repo is already linked to a follower directory')

    follower_path.mkdir()
    Repo.init(follower_path)

    to_follower_symlink.symlink_to(follower_path)
    to_source_symlink.symlink_to(source_path)

    # TODO: add the source symink to the follower directory to .gitignore

    print('Success! New env-tracker repository initialized at {0}'.format(follower_path))
