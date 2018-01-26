import os
from pathlib import Path

from config import config
from main import cmd_init
from tests.helpers import BaseTestCase, init_git_repo, remove_test_folder


class TestInitCommand(BaseTestCase):
    def test_can_init(self):
        """
        Default use case where user successfully invokes `et init`
        with the minimal parameters.
        """
        self.assertFalse(self.child_dir.exists(), 'Child dir should not exist')
        self.assertTrue(self.project_dir.joinpath('.git'), 'Project should be a git repo')

        result = self.runner.invoke(cmd_init, [])
        if result.exception:
            raise result.exception

        self.assertEqual(0, result.exit_code, 'Expect no errors')

        self.assertTrue(self.child_dir.exists(), 'Child dir should have been created')
        self.assertTrue(self.child_dir.is_dir(), 'Child dir should be a dir')
        self.assertTrue(self.child_dir.joinpath('.git').exists(), 'Child dir should be a git repo')
        self.assertTrue(self.child_dir.joinpath('.git').is_dir())
        self.assertTrue(self.child_dir.joinpath(config.PARENT_SYMLINK_NAME).exists(),
                        'Child dir should have a symlink back to the project')
        self.assertTrue(self.child_dir.joinpath(config.PARENT_SYMLINK_NAME).samefile(self.project_dir),
                        'Child dir symlink should point back to the project')

    def test_cannot_init_without_git(self):
        """
        The user may not call init on a directory that isn't a git project root
        """
        remove_test_folder(self.project_dir.joinpath('.git'))
        result = self.runner.invoke(cmd_init, [])

        self.assertNotEqual(0, result.exit_code, 'Expected error when project is not a git repo')
        self.assertIsNotNone(result.exception, 'There should have been an exception')
        self.assertIn('Not a git repository', result.output,
                      'Expecting error output to mention project is not a git repo')

    def test_cannot_init_if_git_project_is_ancestor(self):
        """
        For the sake of being explicit, the user must pass the git project root
        directly, not one of its subdirectories.

        Aside from just "explicit > implicit", this removes potential for
        complication with git submodules.
        """
        project_subdir = self.project_dir.joinpath('some_subdir')
        project_subdir.mkdir()

        self.assertFalse(project_subdir.joinpath('.git').exists(), 'Expected provided directory to not be a git repo')
        self.assertTrue(project_subdir.parent.joinpath('.git').exists(),
                        'Expect provided directory to be the child of a git repo')

        result = self.runner.invoke(cmd_init, [str(project_subdir.absolute())])

        self.assertNotEqual(0, result.exit_code, 'Expected error')
        self.assertIn('Not a git repository. Did you mean this?', result.output,
                      'Expecting error output to mention project is not a git repo')

    def test_cannot_init_if_child_dir_already_exists(self):
        """
        For safety, a user may not init a project whose name already exists in ET_HOME
        """
        init_git_repo(self.project_dir)
        self.assertFalse(self.child_dir.exists())
        self.child_dir.mkdir()

        result = self.runner.invoke(cmd_init, [])
        self.assertNotEqual(0, result.exit_code, 'Expected error when child dir already exists')
        self.assertIn('already exists', result.output, 'Expect error output to say the child dir already exists')

    def test_cannot_init_if_any_child_dir_tracks_that_project(self):
        """
        For safety, a user may not init a project that already has a child dir
        tracking it (PARENT_SYMLINK_NAME points to that dir).
        Otherwise, there would be ambiguity as to which child dir is being used by the project
        """
        other_child_dir = Path(self.ET_HOME).joinpath('something-else')
        pretest_result = self.runner.invoke(cmd_init, ['-n', other_child_dir.name])
        if pretest_result.exception:
            raise pretest_result.exception
        self.assertEqual(0, pretest_result.exit_code)

        self.assertFalse(self.child_dir.exists())
        self.assertTrue(other_child_dir.joinpath('.source').samefile(self.project_dir),
                        'The other child directory should be tracking the project dir')

        result = self.runner.invoke(cmd_init, [])

        self.assertNotEqual(0, result.exit_code, 'Expected error exit code')
        self.assertIn('Conflict: specified directory is already linked to', result.output)

    def test_can_provide_relative_directory(self):
        """
        By default, project pairs are initialized in the cwd.
        A user may specify a different path to initialize.
        The provided directory may be a relative path to the cwd.
        """
        cwd = self.test_dir
        os.chdir(cwd)

        self.assertFalse(Path().absolute().samefile(self.project_dir), 'CWD should not be in the project_dir')
        self.assertFalse(self.child_dir.exists(), 'Child dir shouldn\'t exist')

        directory_param = self.project_dir.absolute().relative_to(Path(cwd).absolute())
        self.assertFalse(directory_param.is_absolute(), 'directory_param should be a relative path')

        result = self.runner.invoke(cmd_init, [str(directory_param)])

        self.assertEqual(0, result.exit_code, 'Expected no errors')
        self.assertTrue(self.child_dir.is_dir(), 'Child dir should have been created')
        self.assertTrue(self.child_dir.joinpath(config.PARENT_SYMLINK_NAME).samefile(self.project_dir),
                        'Child dir should link to project dir')
        self.assertTrue(self.child_dir.joinpath('.git').is_dir(), 'Child dir should be a git repo')

    def test_can_provide_absolute_directory(self):
        """
        By default, project pairs are initialized in the cwd.
        A user may specify a different path to initialize.
        The provided directory may be an absolute path.
        """
        os.chdir(self.test_dir)

        self.assertFalse(Path().absolute().samefile(self.project_dir), 'CWD should not be in the project_dir')
        self.assertFalse(self.child_dir.exists(), 'Child dir shouldn\'t exist')

        directory_param = self.project_dir
        self.assertTrue(directory_param.is_absolute(), 'project_dir should be an absolute path')

        result = self.runner.invoke(cmd_init, [str(directory_param)])

        self.assertEqual(0, result.exit_code, 'Expected no errors')
        self.assertTrue(self.child_dir.is_dir(), 'Child dir should have been created')
        self.assertTrue(self.child_dir.joinpath(config.PARENT_SYMLINK_NAME).samefile(self.project_dir),
                        'Child dir should link to project dir')
        self.assertTrue(self.child_dir.joinpath('.git').is_dir(), 'Child dir should be a git repo')

    #
    # def test_can_specify_a_name(self):
    #     """
    #     A user may specify a custom directory name to be created in ET_HOME.
    #
    #     As of writing,
    #     """
    #     self.fail('Not Implemented')
    #
    # def test_cannot_specify_a_name_with_path_delimiter(self):
    #     """
    #     A user may not specify a name with a path delimiter (e.g. / )
    #     because all tracked repos must be in the top level of
    #     ET_HOME for discovery
    #     """
    #     self.fail('Not Implemented')
