"""
For unit testing the test helpers
"""
import unittest

from tests.helpers import create_test_workspace, flush_test_workspace


class TestTestHelpers(unittest.TestCase):
    def test_todo(self):
        self.fail('Add some unit tests for the test helpers')


class TestRemoveTestFolder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        create_test_workspace()

    @classmethod
    def tearDownClass(cls):
        flush_test_workspace()

