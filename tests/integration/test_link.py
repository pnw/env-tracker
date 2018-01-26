from tests.helpers import BaseTestCase


class TestLink(BaseTestCase):
    def test_can_link(self):
        """
        Default use case where user invokes `et link` with minimal parameters
        """
        self.fail('Not Implemented')

    def test_requires_a_file_argument(self):
        """
        A user must pass a file argument
        """
        self.fail('Not Implemented')

    def test_file_must_exist(self):
        """
        File argument must exist
        """
        self.fail('Not Implemented')

    def test_file_argument_can_be_a_file(self):
        """
        File argument can be a file
        """
        self.fail('Not Implemented')

    def test_file_argument_can_be_a_dir(self):
        """
        File argument can be a directory
        """
        self.fail('Not Implemented')

    def test_file_argument_may_not_be_a_symlink(self):
        """
        Not sure what the use case of allowing symlinks would be...
        """
        self.fail('Not Implemented')

    def test_cannot_link_file_thats_already_linked(self):
        """
        Cannot link something that's already been linked
        """
        self.fail('Not Implemented')


