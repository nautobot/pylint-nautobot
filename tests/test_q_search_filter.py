"""Tests for use of SearchFilter on NautobotFilterSets instead of custom `q` search functions.."""

from pylint.testutils import CheckerTestCase

from pylint_nautobot.q_search_filter import NautobotUseSearchFilterChecker

from .utils import assert_error_file, assert_good_file, parametrize_error_files, parametrize_good_files

_EXPECTED_ERRORS = {
    "filter_set": {
        "msg_id": "nb-no-char-filter-q",
        "line": 8,
        "col_offset": 4,
        "node": lambda module_node: module_node.body[2].body[0],
    },
    "filter_set2": {
        "msg_id": "nb-use-search-filter",
        "line": 16,
        "col_offset": 4,
        "node": lambda module_node: module_node.body[2].body[0],
    },
    "filter_set3": {
        "msg_id": "nb-no-search-function",
        "line": 7,
        "col_offset": 4,
        "node": lambda module_node: module_node.body[2].body[0],
    },
}


class TestNautobotUseSearchFilterChecker(CheckerTestCase):
    """Test blank and null StringField checker."""

    CHECKER_CLASS = NautobotUseSearchFilterChecker

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_error(self, filename, expected_error):
        assert_error_file(self, filename, expected_error)

    @parametrize_good_files(__file__)
    def test_good(self, filename):
        assert_good_file(self, filename)
