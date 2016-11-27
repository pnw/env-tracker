from git import Repo
from logger import log
import os

HOME_DIR = os.path.expanduser('~')

ET_DIR = os.path.join(HOME_DIR, '.et')


def init():
    """
    Initialized a project
    """
    project_name = os.path.split(os.getcwd())[-1]
    log.info('Creating project with name: {}'.format(project_name))
    et_path = os.path.join(ET_DIR, project_name)
    log.info('ET path: {}'.format(et_path))
    if not os.path.exists(et_path):
        log.debug('ET path didn\'t exist. Creating')
        os.makedirs(et_path)
    else:
        print('Project already exists: {0}'.format(et_path))
        return

    log.info('Initializing empty git repo at: {}'.format(et_path))
    Repo.init(et_path)

    print('New env-tracker repository initialized at {0}'.format(et_path))
