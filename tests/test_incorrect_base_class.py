"""Tests for incorrect base class checker."""
import astroid
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest

from pylint_nautobot.incorrect_base_class import NautobotIncorrectBaseClassChecker


class TestIncorrectBaseClassChecker(CheckerTestCase):
    """Test model label construction checker."""

    CHECKER_CLASS = NautobotIncorrectBaseClassChecker

    def test_incorrect_base_class(self):
        test_code = "from django.db.models import Model\n\n\nclass MyModel(Model):\n    pass"
        module_node = astroid.parse(test_code)
        class_node = module_node.body[1]  # type: ignore
        with self.assertAddsMessages(
            MessageTest(
                msg_id="nb-incorrect-base-class",
                node=class_node,
                line=4,
                end_line=4,
                col_offset=0,
                end_col_offset=13,
            ),
        ):
            self.walk(module_node)

    def test_no_issues(self):
        test_code = "from nautobot.core.models import BaseModel\n\n\nclass MyModel(BaseModel):\n    pass"
        module_node = astroid.parse(test_code)
        with self.assertNoMessages():
            self.walk(module_node)
