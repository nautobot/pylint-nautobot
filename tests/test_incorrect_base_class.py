"""Tests for incorrect base class checker."""

from pylint.testutils import CheckerTestCase

from pylint_nautobot.incorrect_base_class import NautobotIncorrectBaseClassChecker

from .utils import assert_error_file
from .utils import assert_good_file
from .utils import parametrize_error_files
from .utils import parametrize_good_files

_EXPECTED_ERRORS = {
    "model": {
        "msg_id": "nb-incorrect-base-class",
        "line": 4,
        "col_offset": 0,
        "node": lambda module_node: module_node.body[1],
        "args": ("django.db.models.base.Model", "nautobot.core.models.BaseModel"),
    },
}


class TestIncorrectBaseClassChecker(CheckerTestCase):
    """Test incorrect base class checker."""

    CHECKER_CLASS = NautobotIncorrectBaseClassChecker

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_sub_class_name(self, path, expected_error):
        assert_error_file(self, path, expected_error)

    @parametrize_good_files(__file__)
    def test_no_issues(self, path):
        assert_good_file(self, path)
