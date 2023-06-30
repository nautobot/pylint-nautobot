"""Tests for incorrect base class checker."""
from pathlib import Path

import astroid
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest
from pytest import mark

from pylint_nautobot.incorrect_base_class import NautobotIncorrectBaseClassChecker

_INPUTS_PATH = Path(__file__).parent / "inputs/incorrect-base-class"
_EXPECTED_ERROR_ARGS = {
    "model": {
        "line": 4,
        "end_line": 4,
        "col_offset": 0,
        "end_col_offset": 14,
        "node": lambda module_node: module_node.body[1],
    },
}


class TestIncorrectBaseClassChecker(CheckerTestCase):
    """Test model label construction checker."""

    CHECKER_CLASS = NautobotIncorrectBaseClassChecker

    @mark.parametrize(
        "filename",
        (file.name for file in _INPUTS_PATH.glob("error_*.py")),
    )
    def test_incorrect_base_class(self, filename):
        name = filename[6:-3]
        test_code = (_INPUTS_PATH / filename).read_text(encoding="utf-8")
        module_node = astroid.parse(test_code)
        expected_args = _EXPECTED_ERROR_ARGS[name]
        node = expected_args.pop("node")
        with self.assertAddsMessages(
            MessageTest(
                msg_id="nb-incorrect-base-class",
                node=node(module_node),
                **expected_args,
            ),
        ):
            self.walk(module_node)

    @mark.parametrize(
        "filename",
        (file.name for file in _INPUTS_PATH.glob("ok_*.py")),
    )
    def test_no_issues(self, filename):
        test_code = (_INPUTS_PATH / filename).read_text(encoding="utf-8")
        module_node = astroid.parse(test_code)
        with self.assertNoMessages():
            self.walk(module_node)
