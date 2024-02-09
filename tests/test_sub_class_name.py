"""Tests for sub class name checker."""

from pylint.testutils import CheckerTestCase

from pylint_nautobot.sub_class_name import NautobotSubClassNameChecker

from .utils import assert_error_file
from .utils import assert_good_file
from .utils import parametrize_error_files
from .utils import parametrize_good_files


def _find_failing_node(module_node):
    return module_node.body[3]


_EXPECTED_ERRORS = {
    "filter_set": {
        "msg_id": "nb-sub-class-name",
        "line": 9,
        "col_offset": 0,
        "args": ("AddressObjectFilterSet",),
        "node": _find_failing_node,
    },
}


class TestSubClassNameChecker(CheckerTestCase):
    """Test sub class name checker"""

    CHECKER_CLASS = NautobotSubClassNameChecker

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_sub_class_name(self, path, expected_error):
        assert_error_file(self, path, expected_error)

    @parametrize_good_files(__file__)
    def test_no_issues(self, path):
        assert_good_file(self, path)
