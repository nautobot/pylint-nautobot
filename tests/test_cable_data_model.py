"""Tests for the Nautobot 3.2 Cable data model checks."""

from pylint.lint import PyLinter
from pylint.testutils import CheckerTestCase

from pylint_nautobot.cable_data_model import NautobotCableDataModelChecker

from .utils import assert_error_file, assert_good_file, parametrize_error_files, parametrize_good_files

_EXPECTED_ERRORS = {
    "q_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 6,
        "end_line": 6,
        "col_offset": 36,
        "end_col_offset": 50,
        "args": ("cable", "cable_termination__cable"),
        "node": lambda module_node: module_node.body[2].body[0].value.args[0],
    },
    "order_by_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 44,
        "end_col_offset": 52,
        "args": ("-cable", "-cable_termination__cable"),
        "node": lambda module_node: module_node.body[1].body[0].value.args[0],
    },
    "values_list_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 47,
        "end_col_offset": 54,
        "args": ("cable", "cable_termination__cable"),
        "node": lambda module_node: module_node.body[1].body[0].value.args[0],
    },
    "get_field_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 6,
        "end_line": 6,
        "col_offset": 37,
        "end_col_offset": 44,
        # `get_field()` resolves one field, so the suggestion is the relation itself rather than a lookup path.
        "args": ("cable", "cable_termination"),
        "node": lambda module_node: module_node.body[1].body[0].value.args[0],
    },
    "get_field_termination_a": {
        "msg_id": "nb-removed-termination-a-b-field",
        "line": 6,
        "end_line": 6,
        "col_offset": 33,
        "end_col_offset": 48,
        "args": ("termination_a",),
        "node": lambda module_node: module_node.body[1].body[0].value.args[0],
    },
    "filter_cable": {
        "msg_id": "nb-deprecated-cable-lookup",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 47,
        "args": ("cable", "cable_termination__isnull=True"),
        "node": lambda module_node: module_node.body[1].body[0].value,
    },
    "select_related_cable": {
        "msg_id": "nb-deprecated-cable-lookup",
        "line": 5,
        "end_line": 5,
        "col_offset": 50,
        "end_col_offset": 65,
        "args": ("cable__status", "cable_termination__cable__status"),
        "node": lambda module_node: module_node.body[1].body[0].value.args[0],
    },
    "cable_assignment": {
        "msg_id": "nb-readonly-cable-attribute",
        "line": 2,
        "end_line": 2,
        "col_offset": 4,
        "end_col_offset": 27,
        "args": ("interface.cable",),
        "node": lambda module_node: module_node.body[0].body[0],
    },
    "create_cable": {
        "msg_id": "nb-readonly-cable-attribute",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 83,
        "args": ("cable",),
        "node": lambda module_node: module_node.body[1].body[0].value,
    },
    "q_termination_a_id": {
        "msg_id": "nb-removed-termination-a-b-field",
        "line": 6,
        "end_line": 6,
        "col_offset": 32,
        "end_col_offset": 64,
        "args": ("termination_a_id",),
        "node": lambda module_node: module_node.body[2].body[0].value.args[0],
    },
    "filter_termination_id_in": {
        "msg_id": "nb-removed-termination-a-b-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 67,
        "args": ("termination_a_id__in",),
        "node": lambda module_node: module_node.body[1].body[0].value,
    },
    "order_by_termination_a_type": {
        "msg_id": "nb-removed-termination-a-b-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 40,
        "end_col_offset": 60,
        "args": ("termination_a_type",),
        "node": lambda module_node: module_node.body[1].body[0].value.args[0],
    },
    "filter_termination_a_id": {
        "msg_id": "nb-deprecated-termination-a-b-lookup",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 62,
        "args": ("termination_a_id",),
        "node": lambda module_node: module_node.body[1].body[0].value,
    },
    "get_termination_type_and_id": {
        "msg_id": "nb-deprecated-termination-a-b-lookup",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 92,
        # Both keywords name the same cable end, so they are reported as a single finding.
        "args": ("termination_a_type, termination_a_id",),
        "node": lambda module_node: module_node.body[1].body[0].value,
    },
    "get_or_create_termination": {
        "msg_id": "nb-deprecated-termination-a-b-lookup",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 98,
        "args": ("termination_a_id",),
        "node": lambda module_node: module_node.body[1].body[0].value,
    },
    "exclude_both_terminations": {
        "msg_id": "nb-termination-a-b-exclude-both-ends",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 95,
        "node": lambda module_node: module_node.body[1].body[0].value,
    },
    "path_lookup": {
        "msg_id": "nb-removed-cable-path-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 58,
        "args": ("cable_paths__is_active",),
        "node": lambda module_node: module_node.body[1].body[0].value,
    },
    "cable_peer_attribute": {
        "msg_id": "nb-removed-cable-peer-field",
        "line": 2,
        "end_line": 2,
        "col_offset": 11,
        "end_col_offset": 32,
        "args": ("_cable_peer",),
        "node": lambda module_node: module_node.body[0].body[0].value,
    },
    "cable_peer_lookup": {
        "msg_id": "nb-removed-cable-peer-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 66,
        "args": ("_cable_peer_type",),
        "node": lambda module_node: module_node.body[1].body[0].value,
    },
}


def test_all_messages_enabled_by_default():
    """Every check is on by default.

    Apps still supporting Nautobot < 3.2 cannot act on the two `nb-deprecated-*-lookup` checks, but they are
    expected to disable those explicitly rather than have them silently absent, so that the suppression is a
    record of intent that can be removed once support for Nautobot < 3.2 is dropped.
    """
    linter = PyLinter()
    linter.register_checker(NautobotCableDataModelChecker(linter))
    symbols = [msg_tuple[1] for msg_tuple in NautobotCableDataModelChecker.msgs.values()]
    assert [symbol for symbol in symbols if not linter.is_message_enabled(symbol)] == []


class TestNautobotCableDataModelChecker(CheckerTestCase):
    """Test the Nautobot 3.2 Cable data model checks."""

    CHECKER_CLASS = NautobotCableDataModelChecker

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_error(self, filename, expected_error):
        assert_error_file(self, filename, expected_error)

    @parametrize_good_files(__file__)
    def test_good(self, filename):
        assert_good_file(self, filename)
