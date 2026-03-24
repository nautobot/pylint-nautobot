"""Tests for tear down super checker."""

from pylint.testutils import CheckerTestCase

from pylint_nautobot.teardown_super import NautobotTearDownSuperChecker

from .utils import assert_error_file, assert_good_file, parametrize_error_files, parametrize_good_files


def _find_teardown_node(module_node):
    """Find the tearDown FunctionDef node."""
    class_node = module_node.body[1]
    return class_node.body[0]


_EXPECTED_ERRORS = {
    "teardown": {
        "versions": ">=2",
        "msg_id": "nb-teardown-super",
        "line": 9,
        "end_line": 9,
        "col_offset": 4,
        "end_col_offset": 16,
        "node": _find_teardown_node,
    },
}


class TestTearDownSuperChecker(CheckerTestCase):
    """Test tear down super checker."""

    CHECKER_CLASS = NautobotTearDownSuperChecker

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_error(self, filename, expected_error):
        assert_error_file(self, filename, expected_error)

    @parametrize_good_files(__file__)
    def test_good(self, filename):
        assert_good_file(self, filename)
