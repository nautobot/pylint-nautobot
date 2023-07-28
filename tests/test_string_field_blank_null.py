"""Tests for blank and null StringFields."""
from pathlib import Path

from pylint.testutils import CheckerTestCase
from pytest import mark

from pylint_nautobot.string_field_blank_null import NautobotStringFieldBlankNull

from .utils import assert_error_file
from .utils import assert_good_file

_INPUTS_PATH = Path(__file__).parent / "inputs/string-field-blank-null/"
_EXPECTED_ERRORS = {
    "field": {
        "msg_id": "nb-string-field-blank-null",
        "line": 5,
        "col_offset": 0,
        "node": lambda module_node: module_node.body[2],
    },
}


class TestStringFieldBlankNullChecker(CheckerTestCase):
    """Test blank and null StringField checker."""

    CHECKER_CLASS = NautobotStringFieldBlankNull

    @mark.parametrize("path", _INPUTS_PATH.glob("error_*.py"))
    def test_string_field_blank_null(self, path):
        assert_error_file(self, path, _EXPECTED_ERRORS)

    @mark.parametrize("path", _INPUTS_PATH.glob("good_*.py"))
    def test_no_issues(self, path):
        assert_good_file(self, path)
