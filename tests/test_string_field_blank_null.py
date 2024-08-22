"""Tests for blank and null StringFields."""

from pylint.testutils import CheckerTestCase

from pylint_nautobot.string_field_blank_null import NautobotStringFieldBlankNull

from .utils import assert_error_file, assert_good_file, parametrize_error_files, parametrize_good_files

_EXPECTED_ERRORS = {
    "field": {
        "msg_id": "nb-string-field-blank-null",
        "line": 6,
        "col_offset": 4,
        "node": lambda module_node: module_node.body[2].body[0],
    },
}


class TestStringFieldBlankNullChecker(CheckerTestCase):
    """Test blank and null StringField checker."""

    CHECKER_CLASS = NautobotStringFieldBlankNull

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_error(self, filename, expected_error):
        assert_error_file(self, filename, expected_error)

    @parametrize_good_files(__file__)
    def test_good(self, filename):
        assert_good_file(self, filename)
