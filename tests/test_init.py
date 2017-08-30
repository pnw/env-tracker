from git import InvalidGitRepositoryError
from tests.base import BaseClass, rmdir
from config import ET_HOME, FOLLOWER_SYMLINK_NAME, PARENT_SYMLINK_NAME

from commands.init import init


class TestInitCommand(BaseClass):
    def test_fails_when_parent_dir_is_not_git(self):
        rmdir(self.parent_proj_path / '.git')
        with self.assertRaises(InvalidGitRepositoryError):
            init(self.parent_proj_path)

    def test_it_lazy_creates_et_files_on_first_run(self):
        self.assertIsNotDir(ET_HOME)
        init(self.parent_proj_path)
        self.assertIsDir(ET_HOME)

    def test_it_initializes_a_child_git_repo(self):
        self.assertIsNotDir(ET_HOME / self.test_proj_name)
        init(self.parent_proj_path)
        self.assertIsDir(ET_HOME / self.test_proj_name)
        self.assertIsDir(ET_HOME / self.test_proj_name / '.git')

    def test_you_can_specify_a_name(self):
        project_name = 'anothername'
        self.assertIsNotDir(self.child_proj_path)
        init(self.parent_proj_path, project_name)
        self.assertIsNotDir(ET_HOME / self.test_proj_name)
        self.assertIsDir(ET_HOME / project_name)
        self.assertIsDir(ET_HOME / project_name / '.git')

    def test_it_links_the_projects_together(self):
        init(self.parent_proj_path)
        link_from_parent = self.parent_proj_path / FOLLOWER_SYMLINK_NAME
        link_from_child = self.child_proj_path / PARENT_SYMLINK_NAME

        self.assertIsSymlink(link_from_parent)
        self.assertIsSymlink(link_from_child)

        self.assertSymlinkResolvesTo(link_from_parent, self.child_proj_path)
        self.assertSymlinkResolvesTo(link_from_child, self.parent_proj_path)
