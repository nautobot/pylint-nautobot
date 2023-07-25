"""Tests for model label construction checker."""
import astroid
from pylint.interfaces import HIGH
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest
from pytest import mark

from pylint_nautobot.model_label import NautobotModelLabelChecker

from .utils import assert_no_message


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
        module_node = astroid.parse(f"NAME = {test_string}\n")
        fnode = module_node.body[0].value  # type: ignore
        with self.assertAddsMessages(
            MessageTest(msg_id="nb-used-model-label-construction", confidence=HIGH, node=fnode, line=1, col_offset=7),
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
        assert_no_message(self, f"NAME = {test_string}\n")
