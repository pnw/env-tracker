import os
import tempfile
import shutil
import unittest
from pathlib import Path

from git import Repo

TMP_PATH = Path(tempfile.TemporaryDirectory().name)

os.environ.update({
    'ET_HOME': str(TMP_PATH / '.et')
})

from config import ET_HOME


class BaseClass(unittest.TestCase):
    test_proj_name = 'test_project'

    TMP_PATH = TMP_PATH

    @property
    def source_proj_path(self) -> Path:
        return TMP_PATH / self.test_proj_name

    @property
    def follower_proj_path(self) -> Path:
        return TMP_PATH / ET_HOME / self.test_proj_name

    def setUp(self):
        clean_mkdir(TMP_PATH)
        clean_mkdir(self.source_proj_path)

        self.assertIsNotDir(ET_HOME)

        # scaffold out a directory to test init on
        Repo.init(self.source_proj_path)

        self.assertIsDir(self.source_proj_path)
        self.assertIsDir(self.source_proj_path, '.git')

    def tearDown(self):
        rmdir(TMP_PATH)

    def assertIsFile(self, path: Path, msg: str = ''):
        if not msg:
            msg = 'expected file to exist: {}'.format(path)
        self.assertTrue(path.is_file(), msg)

    def assertIsNotFile(self, path: Path, msg: str = ''):
        if not msg:
            msg = 'expected file to not exist: {}'.format(path)
        self.assertFalse(path.is_file(), msg)

    def assertPathDoesNotExist(self, path: Path, msg: str = ''):
        if not msg:
            msg = 'expected location to not exist: {}'.format(path)
        self.assertFalse(path.exists(), msg)

    def assertIsDir(self, path: Path, msg: str = ''):
        if not msg:
            msg = 'expected directory to exist: {}'.format(path)
        self.assertTrue(path.is_dir(), msg)

    def assertIsNotDir(self, path: Path, msg: str = ''):
        if not msg:
            msg = 'expected directory to not exist: {}'.format(path)
        self.assertFalse(path.is_dir(), msg)

    def assertIsSymlink(self, path: Path, msg: str = ''):
        if not msg:
            msg = 'expected location to be a symlink: {}'.format(path)
        self.assertTrue(path.is_symlink(), msg)

    def assertIsNotSymlink(self, path: Path, msg: str = ''):
        if not msg:
            msg = 'expected location to not be a symlink: {}'.format(path)
        self.assertFalse(path.is_symlink(), msg)

    def assertSymlinkResolvesTo(self, symlink_path: Path, resolution: Path, msg: str = ''):
        if not msg:
            msg = 'expected symlink\n{}\nto resolve to\n{}\nbut resolves to\n{}\n'.format(symlink_path, resolution, symlink_path.resolve())

        self.assertTrue(symlink_path.resolve() == Path(resolution).resolve(), msg)



def rmdir(path: Path) -> bool:
    if (path.is_dir()):
        shutil.rmtree(str(path), ignore_errors=True)
        return True
    return False


def clean_mkdir(path: Path) -> Path:
    rmdir(path)
    path.mkdir(parents=True)
    return path
