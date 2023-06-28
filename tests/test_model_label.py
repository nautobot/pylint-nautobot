"""Tests for model label construction checker."""
import astroid
from pylint.interfaces import HIGH
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest
from pytest import mark

from pylint_nautobot.model_label import NautobotModelLabelChecker


_COL_OFFSET = 11


class TestModelLabelChecker(CheckerTestCase):
    """Test model label construction checker."""

    CHECKER_CLASS = NautobotModelLabelChecker

    @mark.parametrize(
        "test_string",
        (
            'f"{model._meta.app_label}.{model._meta.model}"',
            'f"Prepended {another_model._meta.app_label}.{another_model._meta.model}, appended"',
        ),
    )
    def test_finds_model_label_construction(self, test_string):
        module_node = astroid.parse(f"def get_label(model, another_model):\n    return {test_string}")
        fnode = module_node.body[0].body[0].value  # type: ignore
        with self.assertAddsMessages(
            MessageTest(
                msg_id="nb-used-model-label-construction",
                confidence=HIGH,
                node=fnode,
                line=2,
                end_line=2,
                col_offset=_COL_OFFSET,
                end_col_offset=_COL_OFFSET + len(test_string),
            ),
        ):
            self.walk(module_node)

    @mark.parametrize(
        "test_string",
        (
            '"{model._meta.app_label}.{model._meta.model}"',
            'f"{model._meta.app_label},{model._meta.model}"',
            'f"{model._meta.app_label}.{another_model._meta.model}"',
        ),
    )
    def test_no_issues(self, test_string):
        module_node = astroid.parse(f"def get_label(model, another_model):\n    return {test_string}")
        with self.assertNoMessages():
            self.walk(module_node)
