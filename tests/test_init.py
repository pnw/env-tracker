import json
import os
from git import InvalidGitRepositoryError
from tests.base import BaseClass, rmdir
from config import ET_HOME, ET_CONFIG_LOCATION

from commands.init import init


class TestInitCommand(BaseClass):
    def test_fails_when_source_dir_is_not_git(self):
        rmdir(self.source_proj_path, '.git')
        with self.assertRaises(InvalidGitRepositoryError):
            init(self.source_proj_path)

    def test_it_lazy_creates_et_files_on_first_run(self):
        self.assertIsNotDir(ET_HOME)
        self.assertIsNotFile(ET_CONFIG_LOCATION)
        init(self.source_proj_path)
        self.assertIsDir(ET_HOME)
        self.assertIsFile(ET_CONFIG_LOCATION)

    def test_it_initializes_a_follower_git_repo(self):
        self.assertIsNotDir(ET_HOME, self.test_proj_name)
        init(self.source_proj_path)
        self.assertIsDir(ET_HOME, self.test_proj_name)
        self.assertIsDir(ET_HOME, self.test_proj_name, '.git')

    def test_you_can_specify_a_name(self):
        project_name = 'anothername'
        self.assertIsNotDir(ET_HOME, project_name)
        init(self.source_proj_path, project_name)
        self.assertIsDir(ET_HOME, project_name)
        self.assertIsDir(ET_HOME, project_name, '.git')

        self.assertIsNotDir(ET_HOME, self.test_proj_name)

    def test_it_registers_the_project_in_etconfig(self):
        project_name = 'someproj'
        self.assertIsNotDir(ET_HOME, project_name)
        init(self.source_proj_path, project_name)

        self.assertIsFile(ET_CONFIG_LOCATION)
        with open(ET_CONFIG_LOCATION, 'r') as f:
            conf_data = json.load(f)

        self.assertIsInstance(conf_data, dict)
        self.assertIsInstance(conf_data.get('projects'), list)
        self.assertEqual(len(conf_data['projects']), 1)

        proj_conf = conf_data['projects'][0]
        self.assertDictEqual(proj_conf, {
            'source_dir': self.source_proj_path,
            'follower_dir': os.path.join(ET_HOME, project_name),
            'name': project_name
        }, 'Unexpected project configuration on et init')
