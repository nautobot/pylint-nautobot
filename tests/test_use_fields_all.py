"""Tests for use fields all"""

from pylint.testutils import CheckerTestCase

from pylint_nautobot.use_fields_all import NautobotUseFieldsAllChecker

from .utils import assert_error_file
from .utils import assert_good_file
from .utils import parametrize_error_files
from .utils import parametrize_good_files


def _find_fields_node(module_node):
    """Find the fields node in the class definition."""
    class_node = module_node.body[3]
    meta = list(class_node.get_children())[3]
    return list(meta.get_children())[1].value


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

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_sub_class_name(self, path, expected_error):
        assert_error_file(self, path, expected_error)

    @parametrize_good_files(__file__)
    def test_no_issues(self, path):
        assert_good_file(self, path)
