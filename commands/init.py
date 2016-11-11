from git import Repo
import os

HOME_DIR = os.path.expanduser('~')

ET_DIR = os.path.join(HOME_DIR, '.et')


def init():
    project_name = os.path.split(os.getcwd())[-1]
    et_path = os.path.join(ET_DIR, project_name)
    if not os.path.exists(et_path):
        os.makedirs(et_path)
    else:
        print('Project already exists: {0}'.format(et_path))
        return

    Repo.init(et_path)

    print('New env-tracker repository initialized at {0}'.format(et_path))
