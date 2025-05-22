"""Tests for incorrect base class checker."""

from pylint.testutils import CheckerTestCase

from pylint_nautobot.incorrect_base_class import NautobotIncorrectBaseClassChecker

from .utils import assert_error_file, assert_good_file, parametrize_error_files, parametrize_good_files


def _find_error_node(module_node):
    return module_node.body[1]


_EXPECTED_ERRORS = {
    "filter_set": {
        "versions": ">=2",
        "msg_id": "nb-incorrect-base-class",
        "line": 4,
        "end_line": 4,
        "col_offset": 0,
        "end_col_offset": 17,
        "node": _find_error_node,
        "args": ("django_filters.filterset.BaseFilterSet", "nautobot.apps.filters.NautobotFilterSet"),
    },
    "form": {
        "versions": ">=2",
        "msg_id": "nb-incorrect-base-class",
        "line": 4,
        "end_line": 4,
        "col_offset": 0,
        "end_col_offset": 12,
        "node": _find_error_node,
        "args": ("django.forms.forms.BaseForm", "nautobot.apps.forms.BootstrapMixin"),
    },
    "model": {
        "versions": ">=2",
        "msg_id": "nb-incorrect-base-class",
        "line": 4,
        "end_line": 4,
        "col_offset": 0,
        "end_col_offset": 13,
        "node": _find_error_node,
        "args": ("django.db.models.base.Model", "nautobot.apps.models.PrimaryModel"),
    },
    "model_form": {
        "versions": ">=2",
        "msg_id": "nb-incorrect-base-class",
        "line": 4,
        "end_line": 4,
        "col_offset": 0,
        "end_col_offset": 17,
        "node": _find_error_node,
        "args": ("django.forms.models.BaseModelForm", "nautobot.apps.forms.NautobotModelForm"),
    },
}


class TestIncorrectBaseClassChecker(CheckerTestCase):
    """Test incorrect base class checker."""

    CHECKER_CLASS = NautobotIncorrectBaseClassChecker

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_error(self, filename, expected_error):
        assert_error_file(self, filename, expected_error)

    @parametrize_good_files(__file__)
    def test_good(self, filename):
        assert_good_file(self, filename)
