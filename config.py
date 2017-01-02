import json
import os
from pathlib import Path

from git import Repo, InvalidGitRepositoryError

from logger import log
from utils import find

ET_FOLLOWER_ROOT_DIR = os.environ.get('ET_FOLLOWER_ROOT_DIR', os.path.join(os.path.expanduser('~'), '.et'))

ET_CONFIG_LOCATION = os.environ.get('ET_CONFIG_LOCATION', os.path.join(ET_FOLLOWER_ROOT_DIR, '.etconfig'))

ET_ROOT_PATH = Path(ET_FOLLOWER_ROOT_DIR)
ET_CONFIG_PATH = Path(ET_CONFIG_LOCATION)


def get_follower_path(project_name):
    return os.path.join(ET_FOLLOWER_ROOT_DIR, project_name)


class Project(object):
    def __init__(self, source_dir: Path, follower_dir: Path, name: str):
        self.source_dir = Path(source_dir).resolve()
        self.follower_dir = Path(follower_dir).resolve()
        self.name = name

    def to_dict(self):
        return {
            'source_dir': str(self.source_dir),
            'follower_dir': str(self.follower_dir),
            'name': self.name
        }


class ETConfig(object):
    def __init__(self, config: dict = None):
        """

        :param config: The parsed json contents of the et config file
        """
        if (not config):
            config = {}
        self._config = config
        self._projects = config.get('projects', [])

    def save(self):
        with open(ET_CONFIG_LOCATION, 'w+') as f:
            json.dump({
                'projects': self._projects
            }, f, indent=4)
        return self

    def register_project(self, source_dir: Path, follower_dir: Path, name: str = ''):
        if not name:
            name = source_dir.name

        if (self.find_project_by_name(name)):
            raise Exception('Project with name {} exists already'.format(name))

        if (self.find_project_by_follower_dir(follower_dir)):
            # err... this should theoretically never happen right?
            raise Exception('{} is already tracking another project'.format(follower_dir))

        if (self.find_project_by_source_dir(source_dir)):
            raise Exception('This repository is already being tracked')

        project = Project(source_dir=source_dir, follower_dir=follower_dir, name=name)

        self._projects.append(project.to_dict())

    def find_project_by_name(self, name: str):
        find(self._projects, lambda proj: proj['name'] == name)
        for project_config in self._projects:
            if (project_config['name'] == name):
                return Project(**project_config)
        return None

    def find_project_by_follower_dir(self, follower_path: Path) -> Project:
        for project_config in self._projects:
            if Path(project_config['follower_dir']) == follower_path:
                return Project(**project_config)
        return None

    def find_project_by_source_dir(self, source_path: Path) -> Project:
        for project_config in self._projects:
            if Path(project_config['source_dir']) == source_path:
                return Project(**project_config)
        return None


def load_et_config() -> ETConfig:
    try:
        with open(ET_CONFIG_LOCATION, 'r') as f:
            return ETConfig(json.load(f))
    except FileNotFoundError:
        return ETConfig()


def is_child_path(parent_path: Path, child_path: Path) -> bool:
    try:
        child_path.relative_to(parent_path)
    except ValueError:
        return False
    else:
        return True


def is_path_in_follower_dir(path: Path) -> bool:
    return is_child_path(ET_ROOT_PATH, path)


def intuit_project_from_path(path: Path) -> Project:
    try:
        repo = Repo(path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        raise

    repo_path = Path(repo.working_dir).resolve()

    config = load_et_config()

    if is_path_in_follower_dir(repo_path):
        project = config.find_project_by_follower_dir(repo_path)
    else:
        project = config.find_project_by_source_dir(repo_path)

    if not project:
        raise Exception('Unknown project')
    return project
