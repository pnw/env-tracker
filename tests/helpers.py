import shutil
import tempfile
import unittest
from pathlib import Path

import os

from click.testing import CliRunner
from git import Repo

from config import config


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        create_test_workspace()
    #
    # @classmethod
    # def tearDownClass(cls):
    #     flush_test_workspace()

    def setUp(self):
        """
        1. Create the dirs we need
        2. Monkey config
        3. Set working directory to the project directory
        """
        self.test_dir: str = tempfile.mkdtemp(dir=test_workspace)

        self.project_dir = Path(self.test_dir).joinpath('project_root')
        self.project_dir.mkdir()

        self.ET_HOME = Path(self.test_dir).joinpath('et-home')
        self.ET_HOME.mkdir()

        self.child_dir = self.ET_HOME.joinpath(self.project_dir.name)

        os.chdir(str(self.project_dir))
        init_git_repo(self.project_dir)
        patch_et_home(self.ET_HOME)
        self.runner = CliRunner()


def init_git_repo(path: Path) -> Repo:
    repo = Repo.init(path)
    repo.index.commit('Hello World')
    return repo


def patch_et_home(location: Path):
    """
    WARNING: This should only be used in tests

    Override the config settings to point ET_HOME to a new value

    :param location: path to set the ET_HOME config value to
    """
    config.ET_HOME = location


test_workspace = Path(tempfile.gettempdir() + '/io.ptrck.env-tracker')


def create_test_workspace() -> Path:
    """
    Creates a namespace in the tempfile directory to be used
    for any temp files or dirs these tests create
    """
    if not test_workspace.exists():
        test_workspace.mkdir(exist_ok=True)

    return test_workspace


def flush_test_workspace():
    """
    Clears out the contents of the temp dir namespace
    created by create_test_dir
    """
    remove_test_folder(test_workspace)


def remove_test_folder(path: Path):
    # Pure paranoia. Don't want to do deleting stuff we don't want to be deleting.
    if not (path.samefile(test_workspace) or test_workspace in path.absolute().parents):
        raise ValueError('Attempting to delete a folder outside of test tempdir workspace')

    # check if folder exists
    if path.exists():
        # remove if exists
        shutil.rmtree(str(path))
