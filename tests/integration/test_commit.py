from tests.helpers import BaseTestCase


class TestCommitCommand(BaseTestCase):
    def test_can_commit(self):
        """
        Default use case where user invokes `et commit` with minimal parameters
        """
        self.fail('Not Implemented')

    def test_does_not_work_outside_of_a_linked_project(self):
        """
        The users cwd must be inside of a project
        """
        self.fail('Not Implemented')
