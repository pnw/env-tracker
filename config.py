import json

from logger import log
from git import Repo, InvalidGitRepositoryError
import os

ET_HOME_DIR = os.environ.get('ET_HOME_DIR', os.path.expanduser('~'))

ET_FOLLOWER_ROOT_DIR = os.environ.get('ET_FOLLOWER_DIR', os.path.join(ET_HOME_DIR, '.et'))

ET_CONFIG_LOCATION = os.environ.get('ET_CONFIG_LOCATION', os.path.join(ET_FOLLOWER_ROOT_DIR, '.etconfig'))

def get_follower_path(project_name):
    return os.path.join(ET_FOLLOWER_ROOT_DIR, project_name)

def find(arr, fn):
    return next((i for i in arr if fn(i)), None)

class CurrentRepo(object):
    def __init__(self):
        try:
            self.repo = Repo(search_parent_directories=True)
        except InvalidGitRepositoryError as e:
            log.debug('TODO: Give better error when we arent in a repo')
            raise

    @property
    def name(self):
        return os.path.split(self.repo.working_dir)[-1]

    @property
    def is_follower(self):
        return os.getcwd().startswith(ET_FOLLOWER_ROOT_DIR)

    @property
    def is_source(self):
        return not self.is_follower

    @property
    def source_path(self):
        if (self.is_source):
            return self.repo.working_dir
        else:
            # TODO: load the settings
            return get_follower_path(self.name)

    @property
    def follower_path(self):
        if (self.is_source):
            return get_follower_path(self.name)
        else:
            return self.repo.working_dir

    def source_repo(self):
        return SourceRepo(self.source_path)

    def follower_repo(self):
        return FollowerRepo(self.follower_path)


class ETConfig(object):
    def __init__(self, config: object = None):
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

    def register_project(self, source_dir: str, follower_dir: str, name: str):
        if (self.find_project_by_name(name)):
            raise Exception('Project with name {} exists already'.format(name))

        if (self.find_project_by_follower_path(follower_dir)):
            # err... this should theoretically never happen right?
            raise Exception('{} is already tracking another project'.format(follower_dir))

        if (self.find_project_by_source_path(source_dir)):
            raise Exception('This repository is already being tracked')

        self._projects.append(dict(
            source_dir=source_dir,
            follower_dir=follower_dir,
            name=name
        ))

    def find_project_by_name(self, name: str):
        return find(self._projects, lambda proj: proj['name'] == name)

    def find_project_by_follower_path(self, follower_dir: str):
        return find(self._projects, lambda proj: proj['follower_dir'] == follower_dir)

    def find_project_by_source_path(self, source_dir: str):
        return find(self._projects, lambda proj: proj['source_dir'] == source_dir)


def get_context():
    try:
        repo = Repo(search_parent_directories=True)
    except InvalidGitRepositoryError as e:
        log.debug('TODO: Give better error when we arent in a repo')
        raise


def load_et_config() -> ETConfig:
    try:
        with open(ET_CONFIG_LOCATION, 'r') as f:
            return ETConfig(json.load(f))
    except FileNotFoundError:
        return ETConfig()


def load_project():
    print('loading project')
    current_repo = CurrentRepo()
    config = load_et_config()

    return Project(config)


class Project(object):
    def __init__(self, settings):
        """
        :param settings:
        :type settings: ProjectSettings
        """
        print('loading project')
        self.settings = settings
        self.source = SourceRepo(settings.source_path)
        self.follower = FollowerRepo(settings.follower_path)


class File(object):
    def __init__(self, project, filepath):
        self.project = project

        abspath = filepath if os.path.isabs(filepath) else os.path.abspath(filepath)
        self.path = os.path.relpath(abspath, project.source.repo.working_directory)


class FollowerRepo(object):
    def __init__(self, path: str):
        self.path = path
        self.repo = Repo(path)


class SourceRepo(object):
    def __init__(self, path: str):
        self.path = path
        self.repo = Repo(path)
