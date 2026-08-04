"""Tests for the Nautobot 3.2 Cable data model checks."""

from astroid.nodes import FunctionDef
from pylint.testutils import CheckerTestCase

from pylint_nautobot.cable_data_model import NautobotCableDataModelChecker

from .utils import assert_error_file, assert_good_file, parametrize_error_files, parametrize_good_files


def _statement(module_node):
    """The offending statement, found by locating the fixture's function rather than by index.

    Every `error_*.py` fixture holds a single function wrapping a single statement, but the number of imports
    preceding it varies, so indexing into `module_node.body` directly would break whenever one is added.
    """
    function = next(node for node in module_node.body if isinstance(node, FunctionDef))
    return function.body[0]


def _call(module_node):
    """The call that the offending statement returns or evaluates."""
    return _statement(module_node).value


def _call_arg(module_node):
    """The call's first positional argument, e.g. the `"cable"` of `order_by("cable")`."""
    return _call(module_node).args[0]


def _nested_call_arg(module_node):
    """The first argument of the expression passed as the call's first keyword, e.g. `Count("cable")`."""
    return _call(module_node).keywords[0].value.args[0]


# Grouped by the message they exercise, in the same order as `NautobotCableDataModelChecker.msgs`, then
# alphabetically within each group, so that the coverage each rule has is visible at a glance.
_EXPECTED_ERRORS = {
    # E4231 nb-removed-cable-field
    "annotate_count_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 7,
        "end_line": 7,
        "col_offset": 48,
        "end_col_offset": 55,
        "args": ("cable", "cable_termination__cable"),
        "node": _nested_call_arg,
    },
    "bulk_update_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 54,
        "end_col_offset": 61,
        # A field-name list, and `cable_termination` is a reverse relation rather than a concrete field.
        "args": ("cable", "CableToCableTermination"),
        "node": lambda module_node: _call(module_node).args[1].elts[0],
    },
    "distinct_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 75,
        "end_col_offset": 82,
        "args": ("cable", "cable_termination__cable"),
        "node": _call_arg,
    },
    "filtered_relation_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 6,
        "end_line": 6,
        "col_offset": 65,
        "end_col_offset": 72,
        "args": ("cable", "cable_termination__cable"),
        "node": _nested_call_arg,
    },
    "get_field_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 6,
        "end_line": 6,
        "col_offset": 37,
        "end_col_offset": 44,
        "args": ("cable", "cable_termination"),
        "node": _call_arg,
    },
    "latest_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 36,
        "end_col_offset": 43,
        "args": ("cable", "cable_termination__cable"),
        "node": _call_arg,
    },
    "order_by_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 44,
        "end_col_offset": 52,
        "args": ("-cable", "-cable_termination__cable"),
        "node": _call_arg,
    },
    "q_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 6,
        "end_line": 6,
        "col_offset": 36,
        "end_col_offset": 50,
        "args": ("cable", "cable_termination__cable"),
        "node": _call_arg,
    },
    "refresh_from_db_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 2,
        "end_line": 2,
        "col_offset": 38,
        "end_col_offset": 45,
        "args": ("cable", "CableToCableTermination"),
        "node": lambda module_node: _call(module_node).keywords[0].value.elts[0],
    },
    "save_update_fields_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 2,
        "end_line": 2,
        "col_offset": 42,
        "end_col_offset": 49,
        # Only the offending element of the list is reported, not the whole call.
        "args": ("cable", "CableToCableTermination"),
        "node": lambda module_node: _call(module_node).keywords[0].value.elts[1],
    },
    "update_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 6,
        "end_line": 6,
        "col_offset": 11,
        "end_col_offset": 69,
        # `update()` resolves against real fields, so even `cable=None` fails here.
        "args": ("cable", "CableToCableTermination"),
        "node": _call,
    },
    "values_list_cable": {
        "msg_id": "nb-removed-cable-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 47,
        "end_col_offset": 54,
        "args": ("cable", "cable_termination__cable"),
        "node": _call_arg,
    },
    # W4232 nb-deprecated-cable-lookup
    "filter_cable": {
        "msg_id": "nb-deprecated-cable-lookup",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 47,
        "args": ("cable", "cable_termination__isnull=True"),
        "node": _call,
    },
    "select_related_cable": {
        "msg_id": "nb-deprecated-cable-lookup",
        "line": 5,
        "end_line": 5,
        "col_offset": 50,
        "end_col_offset": 65,
        "args": ("cable__status", "cable_termination__cable__status"),
        "node": _call_arg,
    },
    # E4233 nb-readonly-cable-attribute
    "cable_assignment": {
        "msg_id": "nb-readonly-cable-attribute",
        "line": 2,
        "end_line": 2,
        "col_offset": 4,
        "end_col_offset": 27,
        "args": ("interface.cable",),
        "node": _statement,
    },
    "create_cable": {
        "msg_id": "nb-readonly-cable-attribute",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 83,
        "args": ("cable",),
        "node": _call,
    },
    # E4234 nb-removed-termination-a-b-field
    "earliest_termination_a_id": {
        "msg_id": "nb-removed-termination-a-b-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 34,
        "end_col_offset": 52,
        "args": ("termination_a_id",),
        "node": _call_arg,
    },
    "filter_termination_id_in": {
        "msg_id": "nb-removed-termination-a-b-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 67,
        "args": ("termination_a_id__in",),
        "node": _call,
    },
    "get_field_termination_a": {
        "msg_id": "nb-removed-termination-a-b-field",
        "line": 6,
        "end_line": 6,
        "col_offset": 33,
        "end_col_offset": 48,
        "args": ("termination_a",),
        "node": _call_arg,
    },
    "order_by_termination_a_type": {
        "msg_id": "nb-removed-termination-a-b-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 40,
        "end_col_offset": 60,
        "args": ("termination_a_type",),
        "node": _call_arg,
    },
    "q_termination_a_id": {
        "msg_id": "nb-removed-termination-a-b-field",
        "line": 6,
        "end_line": 6,
        "col_offset": 32,
        "end_col_offset": 64,
        "args": ("termination_a_id",),
        "node": _call_arg,
    },
    # W4235 nb-deprecated-termination-a-b-lookup
    "filter_termination_a_id": {
        "msg_id": "nb-deprecated-termination-a-b-lookup",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 62,
        "args": ("termination_a_id",),
        "node": _call,
    },
    "get_or_create_termination": {
        "msg_id": "nb-deprecated-termination-a-b-lookup",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 98,
        "args": ("termination_a_id",),
        "node": _call,
    },
    "get_termination_type_and_id": {
        "msg_id": "nb-deprecated-termination-a-b-lookup",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 92,
        # Both keywords name the same cable end, so they are reported as a single finding.
        "args": ("termination_a_type, termination_a_id",),
        "node": _call,
    },
    # W4236 nb-termination-a-b-exclude-both-ends
    "exclude_both_terminations": {
        "msg_id": "nb-termination-a-b-exclude-both-ends",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 95,
        "node": _call,
    },
    # E4237 nb-removed-cable-path-field
    "path_lookup": {
        "msg_id": "nb-removed-cable-path-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 58,
        "args": ("_path__is_active", "cable_paths__is_active"),
        "node": _call,
    },
    # E4238 nb-removed-cable-peer-field
    "cable_peer_attribute": {
        "msg_id": "nb-removed-cable-peer-field",
        "line": 2,
        "end_line": 2,
        "col_offset": 11,
        "end_col_offset": 32,
        "args": ("_cable_peer",),
        "node": _call,
    },
    "cable_peer_lookup": {
        "msg_id": "nb-removed-cable-peer-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 66,
        "args": ("_cable_peer_type",),
        "node": _call,
    },
}


def test_every_message_has_an_error_fixture():
    """Each message should be exercised by at least one `error_*.py` fixture."""
    covered = {expected["msg_id"] for expected in _EXPECTED_ERRORS.values()}
    symbols = {msg_tuple[1] for msg_tuple in NautobotCableDataModelChecker.msgs.values()}
    assert symbols - covered == set()


class TestNautobotCableDataModelChecker(CheckerTestCase):
    """Test the Nautobot 3.2 Cable data model checks."""

    CHECKER_CLASS = NautobotCableDataModelChecker

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_error(self, filename, expected_error):
        assert_error_file(self, filename, expected_error)

    @parametrize_good_files(__file__)
    def test_good(self, filename):
        assert_good_file(self, filename)
