import json
import unittest
import os
import shutil
from pprint import pprint
from git import Repo, InvalidGitRepositoryError

TMP_DIR = '/tmp/et'

SOURCE_PROJ = '/tmp/et/testproject'

os.environ.update({'ET_HOME_DIR': '/tmp/et'})

from config import ET_FOLLOWER_ROOT_DIR, ET_CONFIG_LOCATION
from commands.init import init




class BaseClass(unittest.TestCase):
    def assertIsFile(self, *path_parts: str, msg: str = ''):
        path = os.path.join(*path_parts)
        if not msg:
            msg = 'expected file to exist: {}'.format(path)
        self.assertTrue(os.path.isfile(path), msg)

    def assertIsNotFile(self, *path_parts: str, msg: str = ''):
        path = os.path.join(*path_parts)
        if not msg:
            msg = 'expected file to not exist: {}'.format(path)
        self.assertFalse(os.path.isfile(path), msg)

    def assertIsDir(self, *path_parts: str, msg: str = ''):
        path = os.path.join(*path_parts)
        if not msg:
            msg = 'expected directory to exist: {}'.format(path)
        self.assertTrue(os.path.isdir(path), msg)

    def assertIsNotDir(self, *path_parts: str, msg: str = ''):
        path = os.path.join(*path_parts)
        if not msg:
            msg = 'expected directory to not exist: {}'.format(path)
        self.assertFalse(os.path.isdir(path), msg)


def rmdir(*path_parts: str):
    path = os.path.join(*path_parts)
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
        return True
    return False

def clean_mkdir(*path_parts: str) -> str:
    path = os.path.join(*path_parts)
    rmdir(path)

    os.makedirs(path)
    return path

class TestHelloWorld(BaseClass):
    def setUp(self):
        clean_mkdir(TMP_DIR)
        clean_mkdir(SOURCE_PROJ)

        self.assertIsNotDir(ET_FOLLOWER_ROOT_DIR)

        # scaffold out a directory to test init on
        Repo.init(SOURCE_PROJ)

        self.assertIsDir(SOURCE_PROJ)
        self.assertIsDir(SOURCE_PROJ, '.git')

    def tearDown(self):
        rmdir('/tmp/et')

    def test_fails_when_source_dir_is_not_git(self):
        rmdir(SOURCE_PROJ)
        os.makedirs(SOURCE_PROJ)
        with self.assertRaises(InvalidGitRepositoryError):
            init(SOURCE_PROJ)

    def test_it_lazy_creates_et_files_on_first_run(self):
        self.assertIsNotDir(ET_FOLLOWER_ROOT_DIR)
        self.assertIsNotFile(ET_CONFIG_LOCATION)
        init(SOURCE_PROJ)
        self.assertIsDir(ET_FOLLOWER_ROOT_DIR)
        self.assertIsFile(ET_CONFIG_LOCATION)

    def test_it_initializes_a_follower_git_repo(self):
        self.assertIsNotDir(ET_FOLLOWER_ROOT_DIR, 'testproject')
        init(SOURCE_PROJ)
        self.assertIsDir(ET_FOLLOWER_ROOT_DIR, 'testproject')
        self.assertIsDir(ET_FOLLOWER_ROOT_DIR, 'testproject', '.git')

    def test_you_can_specify_a_name(self):
        project_name = 'anothername'

        self.assertIsNotDir(ET_FOLLOWER_ROOT_DIR, project_name)
        init(SOURCE_PROJ, project_name)
        self.assertIsDir(ET_FOLLOWER_ROOT_DIR, project_name)
        self.assertIsDir(ET_FOLLOWER_ROOT_DIR, project_name, '.git')

        self.assertIsNotDir(ET_FOLLOWER_ROOT_DIR, 'testproject')

    def test_it_registers_the_project_in_etconfig(self):
        project_name = 'someproj'
        self.assertIsNotDir(ET_FOLLOWER_ROOT_DIR, project_name)
        init(SOURCE_PROJ, project_name)

        self.assertIsFile(ET_CONFIG_LOCATION)
        with open(ET_CONFIG_LOCATION, 'r') as f:
            conf_data = json.load(f)
            print(conf_data)

        self.assertIsInstance(conf_data, dict)
        self.assertIsInstance(conf_data.get('projects'), list)
        self.assertEqual(len(conf_data['projects']), 1)

        proj_conf = conf_data['projects'][0]
        self.assertDictEqual(proj_conf, {
            'source_dir': SOURCE_PROJ,
            'follower_dir': os.path.join(ET_FOLLOWER_ROOT_DIR, project_name),
            'name': project_name
        }, 'Unexpected project configuration on et init')
