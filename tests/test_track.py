from pathlib import Path

from tests.base import BaseClass
from commands.init import init
from commands.track import track


class TestTrackCommand(BaseClass):
    def make_test_file(self, relpath: [str, Path]) -> Path:
        relpath = Path(relpath)
        source_file = self.source_proj_path / relpath
        source_file.parent.mkdir(parents=True, exist_ok=True)
        source_file.touch()
        return relpath

    def setUp(self):
        super().setUp()
        init(self.source_proj_path)

    def test_it_works_on_directories(self):
        rel_subdir = Path('test_subdir')
        source_subdir = self.source_proj_path / rel_subdir
        source_subdir.mkdir()

        follower_subdir = self.follower_proj_path / rel_subdir

        self.assertIsDir(source_subdir)
        self.assertPathDoesNotExist(follower_subdir)

        track(source_subdir)

        self.assertIsSymlink(source_subdir)
        self.assertIsDir(follower_subdir)
        self.assertSymlinkResolvesTo(source_subdir, follower_subdir)

    def test_it_works_on_absolute_paths(self):
        file = self.make_test_file(Path('somefile.txt'))
        follower_file_loc = self.follower_proj_path / file
        source_file_loc = self.source_proj_path / file

        self.assertIsAbsolutePath(source_file_loc)
        self.assertIsFile(source_file_loc)

        track(source_file_loc)

        self.assertPathExists(follower_file_loc)
        self.assertIsNotSymlink(follower_file_loc)

        self.assertIsSymlink(source_file_loc)
        self.assertSymlinkResolvesTo(source_file_loc, follower_file_loc)

    def test_it_works_on_relative_paths(self):
        file = self.make_test_file(Path('somefile.txt'))

        follower_file_loc = self.follower_proj_path / file
        source_file_loc = self.source_proj_path / file

        self.assertIsNotAbsolutePath(file)

        track(file)

        self.assertPathExists(follower_file_loc)
        self.assertIsNotSymlink(follower_file_loc)

        self.assertIsSymlink(source_file_loc)
        self.assertSymlinkResolvesTo(source_file_loc, follower_file_loc)

    def test_it_works_on_nested_files(self):
        file = self.make_test_file(Path('some_dir/somefile.txt'))
        self.assertIsFile(self.source_proj_path / file)

    def test_it_fails_for_non_existent_file(self):
        file = self.source_proj_path / Path('doesntexist.txt')
        self.assertPathDoesNotExist(file)

        with self.assertRaisesRegex(FileNotFoundError, 'Path does not exist'):
            track(file)

    def test_it_fails_if_path_is_symlink(self):
        source_file = self.make_test_file(Path('somefile.txt'))
        file = self.source_proj_path / Path('linked_path')
        file.symlink_to(source_file)

        self.assertPathExists(file)

        with self.assertRaisesRegex(Exception, 'File is already symlinked'):
            track(file)

    def test_it_fails_on_files_outside_of_source_project(self):
        with self.assertRaisesRegex(Exception, 'Not in a project'):
            track('..')

    def test_it_fails_if_destination_path_exists(self):
        file = self.make_test_file(Path('somefile.txt'))
        follower_path = self.follower_proj_path / file
        follower_path.touch()

        with self.assertRaisesRegex(Exception, 'Something else already exists at:'):
            track(file)
