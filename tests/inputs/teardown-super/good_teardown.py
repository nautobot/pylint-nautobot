"""Test class with proper tearDown calling super().tearDown()."""

from unittest import TestCase


class MyTestCase(TestCase):
    """Test case with proper tearDown."""

    def tearDown(self):
        """Tear down test fixtures."""
        super().tearDown()
