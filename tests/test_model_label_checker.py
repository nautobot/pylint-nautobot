"""Tests for model label construction checker."""
import astroid
from pylint.interfaces import HIGH
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest
from pytest import mark

from pylint_nautobot.model_label_checker import NautobotModelLabelChecker


_COL_OFFSET = 11


class TestModelLabelChecker(CheckerTestCase):
    """Test model label construction checker."""

    CHECKER_CLASS = NautobotModelLabelChecker

    @mark.parametrize(
        "test_fstring",
        (
            "{model._meta.app_label}.{model._meta.model}",
            "Prepended {another_model._meta.app_label}.{another_model._meta.model}, appended",
        ),
    )
    def test_finds_model_label_construction(self, test_fstring):
        module_node = astroid.parse('def get_label(model, another_model):\n    return f"' + test_fstring + '"')
        fnode = module_node.body[0].body[0].value  # type: ignore
        with self.assertAddsMessages(
            MessageTest(
                msg_id="used-model-label-construction",
                confidence=HIGH,
                node=fnode,
                line=2,
                end_line=2,
                col_offset=_COL_OFFSET,
                end_col_offset=_COL_OFFSET + len(test_fstring) + 3,
            ),
        ):
            self.walk(module_node)

    @mark.parametrize(
        "test_fstring",
        (
            "{model._meta.app_label},{model._meta.model}",
            "{model._meta.app_label}.{another_model._meta.model}",
        ),
    )
    def test_ignores_non_model_label_construction(self, test_fstring):
        module_node = astroid.parse('def get_label(model, another_model):\n    return f"' + test_fstring + '"')
        with self.assertNoMessages():
            self.walk(module_node)
