"""Test version specifier parsing."""

import pytest
from packaging.specifiers import InvalidSpecifier, SpecifierSet

from pylint_nautobot import CHECKERS


def test_version_specifiers():
    for checker in CHECKERS:
        try:
            SpecifierSet(checker.version_specifier)
        except InvalidSpecifier:
            pytest.fail(f"Version specifier {checker.version_specifier} doesn't parse.")
