"""Tests for deprecated status model."""

from pylint.testutils import CheckerTestCase

from pylint_nautobot.deprecated_status_model import NautobotDeprecatedStatusModelChecker

from .utils import assert_error_file
from .utils import assert_good_file
from .utils import parametrize_error_files
from .utils import parametrize_good_files

_EXPECTED_ERRORS = {
    "status_model": {
        "msg_id": "nb-status-field-instead-of-status-model",
        "line": 4,
        "col_offset": 0,
        "node": lambda module_node: module_node.body[1],
    },
}


class TestDeprecatedStatusModelChecker(CheckerTestCase):
    """Test deprecated status model checker."""

    CHECKER_CLASS = NautobotDeprecatedStatusModelChecker

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_sub_class_name(self, path, expected_error):
        assert_error_file(self, path, expected_error)

    # TBD: Missing test for good_status_model.py
    @parametrize_good_files(__file__)
    def test_no_issues(self, path):
        assert_good_file(self, path)
