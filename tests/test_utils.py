import tempfile
import unittest
from pathlib import Path

import os

from click.testing import CliRunner

from tests.monkey import patch_et_home
from tests.workspace import test_workspace, flush_test_workspace, create_test_workspace


class BaseTestCase(unittest.TestCase):
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
