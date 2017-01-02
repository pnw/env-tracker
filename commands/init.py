from git import Repo, InvalidGitRepositoryError
from logger import log
from config import get_follower_path, load_et_config
import os


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

    if (not project_name):
        project_name = os.path.split(repo.working_dir)[-1]
    follower_dir = get_follower_path(project_name)

    log.info('Creating project with name: {}'.format(project_name))
    log.info('ET path: {}'.format(follower_dir))

    try:
        log.info('Creating new ET project at: {}'.format(follower_dir))
        os.makedirs(follower_dir)
    except FileExistsError:
        print('Project already exists')

    log.info('Initializing empty git repo at: {}'.format(follower_dir))
    Repo.init(follower_dir)

    log.info('Creating config file')
    config = load_et_config()

    config.register_project(
        source_dir=repo.working_dir,
        follower_dir=follower_dir,
        name=project_name
    )
    config.save()

    print('Success! New env-tracker repository initialized at {0}'.format(follower_dir))
