import os
import shutil
import unittest

from git import Repo

TMP_DIR = str('/private/tmp/et_test')

os.environ.update({
    'ET_FOLLOWER_ROOT_DIR': os.path.join(TMP_DIR, '.et')
})

from config import ET_FOLLOWER_ROOT_DIR


class BaseClass(unittest.TestCase):
    test_proj_name = 'testproject'

    @property
    def source_proj_path(self):
        return os.path.join(TMP_DIR, self.test_proj_name)

    def setUp(self):
        clean_mkdir(TMP_DIR)
        clean_mkdir(self.source_proj_path)

        self.assertIsNotDir(ET_FOLLOWER_ROOT_DIR)

        # scaffold out a directory to test init on
        Repo.init(self.source_proj_path)

        self.assertIsDir(self.source_proj_path)
        self.assertIsDir(self.source_proj_path, '.git')

    def tearDown(self):
        rmdir(TMP_DIR)

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
