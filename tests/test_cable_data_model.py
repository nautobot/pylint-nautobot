"""Tests for the Nautobot 3.2 Cable data model checks."""

from astroid.nodes import FunctionDef
from pylint.testutils import CheckerTestCase

from pylint_nautobot.cable_data_model import NautobotCableDataModelChecker

from .utils import assert_error_file, assert_good_file, parametrize_error_files, parametrize_good_files


def _function(module_node):
    """The fixture's function, found by type rather than by index.

    The number of imports preceding it varies between fixtures, so indexing into `module_node.body` directly
    would break whenever one is added.
    """
    return next(node for node in module_node.body if isinstance(node, FunctionDef))


def _statement(module_node):
    """The offending statement, which in most fixtures is the only one in the function."""
    return _function(module_node).body[0]


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
    # E4230 nb-removed-cable-field
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
    # E4231 nb-readonly-cable-attribute
    "inferred_cable_assignment": {
        "msg_id": "nb-readonly-cable-attribute",
        "line": 7,
        "end_line": 7,
        "col_offset": 4,
        "end_col_offset": 27,
        # The target infers to `Interface`, so the failure is confirmed rather than suspected.
        "args": ("interface.cable",),
        "node": lambda module_node: _function(module_node).body[1],
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
    # E4232 nb-removed-termination-a-b-field
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
    # E4233 nb-removed-cable-path-field
    "path_lookup": {
        "msg_id": "nb-removed-cable-path-field",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 58,
        "args": ("_path__is_active", "cable_paths__is_active"),
        "node": _call,
    },
    # E4234 nb-removed-cable-peer-field
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
    # W4235 nb-deprecated-cable-lookup
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
    # W4236 nb-possible-readonly-cable-attribute
    "possible_cable_assignment": {
        "msg_id": "nb-possible-readonly-cable-attribute",
        "line": 2,
        "end_line": 2,
        "col_offset": 4,
        "end_col_offset": 27,
        # A bare parameter cannot be inferred, so the failure is suspected rather than confirmed.
        "args": ("interface.cable",),
        "node": _statement,
    },
    # W4237 nb-deprecated-termination-a-b-lookup
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
    # W4238 nb-termination-a-b-exclude-both-ends
    "exclude_both_terminations": {
        "msg_id": "nb-termination-a-b-exclude-both-ends",
        "line": 5,
        "end_line": 5,
        "col_offset": 11,
        "end_col_offset": 95,
        "node": _call,
    },
    # W4239 nb-possible-removed-field
    "possible_update_cable": {
        "msg_id": "nb-possible-removed-field",
        "line": 3,
        "end_line": 3,
        "col_offset": 4,
        "end_col_offset": 32,
        # No replacement is offered, since a dict receiver would have nothing to migrate.
        "args": ("cable",),
        "node": _call,
    },
}


# Recognising a join model record by inferring a local's type only works where astroid can resolve the class, so
# fixtures relying on that are gated. Recognising it by name works on every version and stays ungated.
_GOOD_FILE_VERSIONS = {
    "inferred_cable_to_cable_termination": ">=3.2",
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

    @parametrize_good_files(__file__, _GOOD_FILE_VERSIONS)
    def test_good(self, filename):
        assert_good_file(self, filename)
