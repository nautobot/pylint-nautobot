"""Tests for use fields all"""

from astroid import Assign
from pylint.testutils import CheckerTestCase

from pylint_nautobot.use_fields_all import NautobotUseFieldsAllChecker
from pylint_nautobot.utils import find_meta

from .utils import assert_error_file
from .utils import assert_good_file
from .utils import parametrize_error_files
from .utils import parametrize_good_files


def _find_fields_node(module_node):
    """Find the fields node in the class definition."""
    class_node = module_node.body[1]
    meta = find_meta(class_node)
    if meta:
        assign = list(meta.get_children())[0]
        if isinstance(assign, Assign):
            return assign.value


_EXPECTED_ERRORS = {
    "filter_set": {
        "msg_id": "nb-use-fields-all",
        "line": 10,
        "col_offset": 17,
        "node": _find_fields_node,
    },
    "form": {
        "msg_id": "nb-use-fields-all",
        "line": 10,
        "col_offset": 17,
        "node": _find_fields_node,
    },
    "serializer": {
        "msg_id": "nb-use-fields-all",
        "line": 10,
        "col_offset": 17,
        "node": _find_fields_node,
    },
}


class TestUseFieldsAllChecker(CheckerTestCase):
    """Test use fields all checker"""

    CHECKER_CLASS = NautobotUseFieldsAllChecker

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_error(self, filename, expected_error):
        assert_error_file(self, filename, expected_error)

    @parametrize_good_files(__file__)
    def test_good(self, filename):
        assert_good_file(self, filename)
