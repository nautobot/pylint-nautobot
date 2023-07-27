"""Tests for deprecated status model."""
from pathlib import Path

from pylint.testutils import CheckerTestCase
from pytest import mark

from pylint_nautobot.deprecated_status_model import NautobotDeprecatedStatusModelChecker

from .utils import assert_error_file
from .utils import assert_good_file

_INPUTS_PATH = Path(__file__).parent / "inputs/deprecated-status-model/"
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

    @mark.parametrize("path", _INPUTS_PATH.glob("error_*.py"))
    def test_deprecated_status_model(self, path):
        assert_error_file(self, path, _EXPECTED_ERRORS)

    # TBD: Missing test for good_status_model.py
    @mark.parametrize("path", _INPUTS_PATH.glob("good_*.py"))
    def test_no_issues(self, path):
        assert_good_file(self, path)
