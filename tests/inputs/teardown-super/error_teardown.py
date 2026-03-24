"""Test class with tearDown that does not call super().tearDown()."""

from unittest import TestCase


class MyTestCase(TestCase):
    """Test case with missing super().tearDown()."""

    def tearDown(self):
        """Tear down test fixtures."""
        pass
