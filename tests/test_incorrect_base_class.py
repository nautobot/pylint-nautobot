"""Tests for incorrect base class checker."""
from pathlib import Path

from pylint.testutils import CheckerTestCase
from pytest import mark

from pylint_nautobot.incorrect_base_class import NautobotIncorrectBaseClassChecker

from .utils import assert_error_file
from .utils import assert_good_file

_INPUTS_PATH = Path(__file__).parent / "inputs/incorrect-base-class"
_EXPECTED_ERROR_ARGS = {
    "model": {
        "msg_id": "nb-incorrect-base-class",
        "line": 4,
        "col_offset": 0,
        "node": lambda module_node: module_node.body[1],
    },
}


class TestIncorrectBaseClassChecker(CheckerTestCase):
    """Test incorrect base class checker."""

    CHECKER_CLASS = NautobotIncorrectBaseClassChecker

    @mark.parametrize("path", _INPUTS_PATH.glob("error_*.py"))
    def test_incorrect_base_class(self, path):
        assert_error_file(self, path, _EXPECTED_ERROR_ARGS)

    @mark.parametrize("path", _INPUTS_PATH.glob("good_*.py"))
    def test_no_issues(self, path):
        assert_good_file(self, path)
