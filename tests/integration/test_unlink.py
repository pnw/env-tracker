from tests.helpers import BaseTestCase


class TestUnlinkCommand(BaseTestCase):
    def test_can_unlink(self):
        """
        Default use case where user invokes `et unlink` with minimal parameters
        """
        self.fail('Not Implemented')

    def test_requires_the_file_argument(self):
        """
        A user must pass the file argument
        """
        self.fail('Not Implemented')

    def test_file_must_exist(self):
        """
        A user must pass a file that exists
        """
        self.fail('Not Implemented')

    def test_file_must_be_linked(self):
        """
        The file must be correctly linked between child dir and project dirs
        """
        self.fail('Not Implemented')
