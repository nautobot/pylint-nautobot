"""Tests for JobResult ForeignKey/OneToOneField PROTECT checker."""

from pylint.testutils import CheckerTestCase

from pylint_nautobot.jobresult_on_delete_protect import NautobotJobResultOnDeleteProtectChecker

from .utils import assert_error_file, assert_good_file, parametrize_error_files, parametrize_good_files

_EXPECTED_ERRORS = {
    "protect_fk_string": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 6,
        "end_line": 6,
        "col_offset": 4,
        "end_col_offset": 80,
        "node": lambda module_node: module_node.body[2].body[0],
    },
    "protect_fk_string_simple": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 6,
        "end_line": 6,
        "col_offset": 4,
        "end_col_offset": 73,
        "node": lambda module_node: module_node.body[2].body[0],
    },
    "protect_fk_direct": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 7,
        "end_line": 7,
        "col_offset": 4,
        "end_col_offset": 71,
        "node": lambda module_node: module_node.body[3].body[0],
    },
    "protect_fk_imported": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 7,
        "end_line": 7,
        "col_offset": 4,
        "end_col_offset": 66,
        "node": lambda module_node: module_node.body[3].body[0],
    },
    "protect_fk_imported_string_extras": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 7,
        "end_line": 7,
        "col_offset": 4,
        "end_col_offset": 73,
        "node": lambda module_node: module_node.body[3].body[0],
    },
    "protect_fk_imported_direct": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 8,
        "end_line": 8,
        "col_offset": 4,
        "end_col_offset": 64,
        "node": lambda module_node: module_node.body[4].body[0],
    },
    "protect_fk_to_keyword": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 6,
        "end_line": 6,
        "col_offset": 4,
        "end_col_offset": 110,
        "node": lambda module_node: module_node.body[2].body[0],
    },
    "protect_fk_to_keyword_simple": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 6,
        "end_line": 6,
        "col_offset": 4,
        "end_col_offset": 76,
        "node": lambda module_node: module_node.body[2].body[0],
    },
    "protect_fk_to_keyword_direct": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 7,
        "end_line": 7,
        "col_offset": 4,
        "end_col_offset": 74,
        "node": lambda module_node: module_node.body[3].body[0],
    },
    "protect_fk_to_keyword_imported": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 7,
        "end_line": 7,
        "col_offset": 4,
        "end_col_offset": 69,
        "node": lambda module_node: module_node.body[3].body[0],
    },
    "protect_fk_to_keyword_imported_extras": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 7,
        "end_line": 7,
        "col_offset": 4,
        "end_col_offset": 76,
        "node": lambda module_node: module_node.body[3].body[0],
    },
    "protect_fk_to_keyword_imported_direct": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 8,
        "end_line": 8,
        "col_offset": 4,
        "end_col_offset": 67,
        "node": lambda module_node: module_node.body[4].body[0],
    },
    "protect_1to1_string": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 6,
        "end_line": 6,
        "col_offset": 4,
        "end_col_offset": 83,
        "node": lambda module_node: module_node.body[2].body[0],
    },
    "protect_1to1_string_simple": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 6,
        "end_line": 6,
        "col_offset": 4,
        "end_col_offset": 76,
        "node": lambda module_node: module_node.body[2].body[0],
    },
    "protect_1to1_direct": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 7,
        "end_line": 7,
        "col_offset": 4,
        "end_col_offset": 74,
        "node": lambda module_node: module_node.body[3].body[0],
    },
    "protect_1to1_imported": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 7,
        "end_line": 7,
        "col_offset": 4,
        "end_col_offset": 69,
        "node": lambda module_node: module_node.body[3].body[0],
    },
    "protect_1to1_imported_string_extras": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 7,
        "end_line": 7,
        "col_offset": 4,
        "end_col_offset": 76,
        "node": lambda module_node: module_node.body[3].body[0],
    },
    "protect_1to1_imported_direct": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 8,
        "end_line": 8,
        "col_offset": 4,
        "end_col_offset": 67,
        "node": lambda module_node: module_node.body[4].body[0],
    },
    "protect_1to1_to_keyword": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 6,
        "end_line": 6,
        "col_offset": 4,
        "end_col_offset": 86,
        "node": lambda module_node: module_node.body[2].body[0],
    },
    "protect_1to1_to_keyword_simple": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 6,
        "end_line": 6,
        "col_offset": 4,
        "end_col_offset": 79,
        "node": lambda module_node: module_node.body[2].body[0],
    },
    "protect_1to1_to_keyword_direct": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 7,
        "end_line": 7,
        "col_offset": 4,
        "end_col_offset": 77,
        "node": lambda module_node: module_node.body[3].body[0],
    },
    "protect_1to1_to_keyword_imported": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 7,
        "end_line": 7,
        "col_offset": 4,
        "end_col_offset": 72,
        "node": lambda module_node: module_node.body[3].body[0],
    },
    "protect_1to1_to_keyword_imported_extras": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 7,
        "end_line": 7,
        "col_offset": 4,
        "end_col_offset": 79,
        "node": lambda module_node: module_node.body[3].body[0],
    },
    "protect_1to1_to_keyword_imported_direct": {
        "msg_id": "nb-jobresult-on-delete-protect",
        "line": 8,
        "end_line": 8,
        "col_offset": 4,
        "end_col_offset": 70,
        "node": lambda module_node: module_node.body[4].body[0],
    },
}


class TestJobResultOnDeleteProtectChecker(CheckerTestCase):
    """Test JobResult ForeignKey/OneToOneField PROTECT checker."""

    CHECKER_CLASS = NautobotJobResultOnDeleteProtectChecker

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_error(self, filename, expected_error):
        assert_error_file(self, filename, expected_error)

    @parametrize_good_files(__file__)
    def test_good(self, filename):
        assert_good_file(self, filename)
