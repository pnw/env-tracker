from git import InvalidGitRepositoryError
from tests.base import BaseClass, rmdir
from config import ET_HOME, FOLLOWER_SYMLINK_NAME, SOURCE_SYMLINK_NAME

from commands.init import init


class TestInitCommand(BaseClass):
    def test_fails_when_source_dir_is_not_git(self):
        rmdir(self.source_proj_path / '.git')
        with self.assertRaises(InvalidGitRepositoryError):
            init(self.source_proj_path)

    def test_it_lazy_creates_et_files_on_first_run(self):
        self.assertIsNotDir(ET_HOME)
        init(self.source_proj_path)
        self.assertIsDir(ET_HOME)

    def test_it_initializes_a_follower_git_repo(self):
        self.assertIsNotDir(ET_HOME / self.test_proj_name)
        init(self.source_proj_path)
        self.assertIsDir(ET_HOME / self.test_proj_name)
        self.assertIsDir(ET_HOME /self.test_proj_name / '.git')

    def test_you_can_specify_a_name(self):
        project_name = 'anothername'
        self.assertIsNotDir(self.follower_proj_path)
        init(self.source_proj_path, project_name)
        self.assertIsNotDir(ET_HOME / self.test_proj_name)
        self.assertIsDir(ET_HOME / project_name)
        self.assertIsDir(ET_HOME / project_name / '.git')


    def test_it_links_the_projects_together(self):
        init(self.source_proj_path)
        link_from_source = self.source_proj_path / FOLLOWER_SYMLINK_NAME
        link_from_follower = self.follower_proj_path / SOURCE_SYMLINK_NAME

        self.assertIsSymlink(link_from_source)
        self.assertIsSymlink(link_from_follower)

        self.assertSymlinkResolvesTo(link_from_source, self.follower_proj_path)
        self.assertSymlinkResolvesTo(link_from_follower, self.source_proj_path)
