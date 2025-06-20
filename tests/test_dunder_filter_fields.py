"""Tests for use of SearchFilter on NautobotFilterSets instead of custom `q` search functions.."""

from pylint.testutils import CheckerTestCase

from pylint_nautobot.dunder_filter_fields import NautobotDunderFilterFieldChecker

from .utils import assert_error_file, assert_good_file, parametrize_error_files, parametrize_good_files

_EXPECTED_ERRORS = {
    "filter_set": {
        "msg_id": "nb-warn-dunder-filter-field",
        "line": 7,
        "end_line": 12,
        "col_offset": 4,
        "end_col_offset": 5,
        "node": lambda module_node: module_node.body[1].body[0],
    },
}


class TestNautobotDunderFilterFieldChecker(CheckerTestCase):
    """Test dunder in FilterSet fields."""

    CHECKER_CLASS = NautobotDunderFilterFieldChecker

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_error(self, filename, expected_error):
        assert_error_file(self, filename, expected_error)

    @parametrize_good_files(__file__)
    def test_good(self, filename):
        assert_good_file(self, filename)
