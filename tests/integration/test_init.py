import tempfile
import unittest
from pathlib import Path

import os
from click.testing import CliRunner
from git import Repo

from config import config
from main import cmd_init
from tests.monkey import patch_et_home
from tests.workspace import create_test_workspace, flush_test_workspace, test_workspace


class TestInitCommand(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        create_test_workspace()

    @classmethod
    def tearDownClass(cls):
        flush_test_workspace()

    def setUp(self):
        """
        1. Create the dirs we need
        2. Monkey config
        3. Set working directory to the project directory
        """
        self.test_dir: str = tempfile.mkdtemp(dir=test_workspace)

        self.project_dir = Path(tempfile.mkdtemp(dir=self.test_dir))
        self.ET_HOME = Path(tempfile.mkdtemp(dir=self.test_dir))
        self.child_dir = self.ET_HOME.joinpath(self.project_dir.name)

        os.chdir(str(self.project_dir))
        patch_et_home(self.ET_HOME)
        self.runner = CliRunner()

    def test_can_init(self):
        """
        Default use case where user successfully invokes `et init`
        with the minimal parameters.
        """
        repo = Repo.init(self.project_dir)
        repo.index.commit('Hello world')
        result = self.runner.invoke(cmd_init, [])
        if result.exception:
            raise result.exception
        self.assertEqual(0, result.exit_code, 'Expect no errors')
        self.assertTrue(self.child_dir.exists())
        self.assertTrue(self.child_dir.is_dir())
        self.assertTrue(self.child_dir.joinpath(config.PARENT_SYMLINK_NAME).exists())
        self.assertTrue(self.child_dir.joinpath(config.PARENT_SYMLINK_NAME).samefile(self.project_dir))

    def test_cannot_init_without_git(self):
        """
        The user may not call init on a directory that isn't a git project root
        """
        self.fail('Not Implemented')

    def test_cannot_init_if_child_dir_already_exists(self):
        """
        For safety, a user may not init a project whose name already exists in ET_HOME
        """
        self.fail('Not Implemented')

    def test_cannot_init_if_any_child_dir_tracks_that_project(self):
        """
        For safety, a user may not init a project that already has a child dir
        tracking it (PARENT_SYMLINK_NAME points to that dir).
        Otherwise, there would be ambiguity as to which child dir is being used by the project
        """
        self.fail('Not Implemented')

    def test_cannot_init_if_git_root_is_parent(self):
        """
        For the sake of being explicit, the user must pass the git project root
        directly, not one of its subdirectories.

        Aside from just "explicit > implicit", this removes potential for
        complication with git submodules.
        """
        self.fail('Not Implemented')

    def test_can_init_outside_of_cwd(self):
        """
        By default, project pairs are initialized in the cwd.
        A user may specify a different path to initialize.
        """
        self.fail('Not Implemented')

    def test_can_specify_a_name(self):
        """
        A user may specify a custom directory name to be created in ET_HOME.

        As of writing,
        """
        self.fail('Not Implemented')

    def test_cannot_specify_a_name_with_path_delimiter(self):
        """
        A user may not specify a name with a path delimiter (e.g. / )
        because all tracked repos must be in the top level of
        ET_HOME for discovery
        """
        self.fail('Not Implemented')
