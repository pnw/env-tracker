from pathlib import Path

from tests.base import BaseClass
from commands.init import init
from commands.track import track


class TestTrackCommand(BaseClass):
    def make_test_file(self, relpath: [str, Path]) -> Path:
        relpath = Path(relpath)
        parent_file = self.parent_proj_path / relpath
        parent_file.parent.mkdir(parents=True, exist_ok=True)
        parent_file.touch()
        return relpath

    def setUp(self):
        super().setUp()
        init(self.parent_proj_path)

    def test_it_works_on_directories(self):
        rel_subdir = Path('test_subdir')
        parent_subdir = self.parent_proj_path / rel_subdir
        parent_subdir.mkdir()

        child_subdir = self.child_proj_path / rel_subdir

        self.assertIsDir(parent_subdir)
        self.assertPathDoesNotExist(child_subdir)

        track(parent_subdir)

        self.assertIsSymlink(parent_subdir)
        self.assertIsDir(child_subdir)
        self.assertSymlinkResolvesTo(parent_subdir, child_subdir)

    def test_it_works_on_absolute_paths(self):
        file = self.make_test_file(Path('somefile.txt'))
        child_file_loc = self.child_proj_path / file
        parent_file_loc = self.parent_proj_path / file

        self.assertIsAbsolutePath(parent_file_loc)
        self.assertIsFile(parent_file_loc)

        track(parent_file_loc)

        self.assertPathExists(child_file_loc)
        self.assertIsNotSymlink(child_file_loc)

        self.assertIsSymlink(parent_file_loc)
        self.assertSymlinkResolvesTo(parent_file_loc, child_file_loc)

    def test_it_works_on_relative_paths(self):
        file = self.make_test_file(Path('somefile.txt'))

        child_file_loc = self.child_proj_path / file
        parent_file_loc = self.parent_proj_path / file

        self.assertIsNotAbsolutePath(file)

        track(file)

        self.assertPathExists(child_file_loc)
        self.assertIsNotSymlink(child_file_loc)

        self.assertIsSymlink(parent_file_loc)
        self.assertSymlinkResolvesTo(parent_file_loc, child_file_loc)

    def test_it_works_on_nested_files(self):
        file = self.make_test_file(Path('some_dir/somefile.txt'))
        self.assertIsFile(self.parent_proj_path / file)

    def test_it_fails_for_non_existent_file(self):
        file = self.parent_proj_path / Path('doesntexist.txt')
        self.assertPathDoesNotExist(file)

        with self.assertRaisesRegex(FileNotFoundError, 'Path does not exist'):
            track(file)

    def test_it_fails_if_path_is_symlink(self):
        parent_file = self.make_test_file(Path('somefile.txt'))
        file = self.parent_proj_path / Path('linked_path')
        file.symlink_to(parent_file)

        self.assertPathExists(file)

        with self.assertRaisesRegex(Exception, 'File is already symlinked'):
            track(file)

    def test_it_fails_on_files_outside_of_parent_project(self):
        with self.assertRaisesRegex(Exception, 'Not in a project'):
            track('..')

    def test_it_fails_if_destination_path_exists(self):
        file = self.make_test_file(Path('somefile.txt'))
        child_path = self.child_proj_path / file
        child_path.touch()

        with self.assertRaisesRegex(Exception, 'Something else already exists at:'):
            track(file)
