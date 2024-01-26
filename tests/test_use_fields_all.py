"""Tests for use fields all"""
from pathlib import Path

from pylint.testutils import CheckerTestCase
from pytest import mark

from pylint_nautobot.use_fields_all import NautobotUseFieldsAllChecker

from .utils import assert_error_file
from .utils import assert_good_file


def _find_fields_node(module_node):
    """Find the fields node in the class definition."""
    class_node = module_node.body[3]
    meta = list(class_node.get_children())[3]
    return list(meta.get_children())[1].value


_INPUTS_PATH = Path(__file__).parent / "inputs/use-fields-all/"
_EXPECTED_ERRORS = {
    "table": {
        "msg_id": "nb-use-fields-all",
        "line": 14,
        "col_offset": 17,
        "node": _find_fields_node,
    },
}


class TestUseFieldsAllChecker(CheckerTestCase):
    """Test use fields all checker"""

    CHECKER_CLASS = NautobotUseFieldsAllChecker

    @mark.parametrize("path", _INPUTS_PATH.glob("error_*.py"))
    def test_use_fields_all(self, path):
        assert_error_file(self, path, _EXPECTED_ERRORS)

    @mark.parametrize("path", _INPUTS_PATH.glob("good_*.py"))
    def test_no_issues(self, path):
        assert_good_file(self, path)
