from tests.helpers import BaseTestCase


class TestStatusCommand(BaseTestCase):
    def test_can_status(self):
        """
        Default use case where user invokes `et status` with minimal parameters
        """
