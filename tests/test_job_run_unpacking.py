"""Tests for job run unpacking checker."""

import astroid
import pytest
from pylint.testutils import CheckerTestCase, MessageTest

from pylint_nautobot.job_run_unpacking import NautobotJobRunUnpackingChecker
from pylint_nautobot.utils import is_version_compatible

from .utils import (
    _INPUTS_PATH as INPUTS_PATH,
)
from .utils import (
    assert_error_file,
    assert_good_file,
    parametrize_error_files,
    parametrize_good_files,
)

_CHECKER_DIR = "job-run-unpacking"


def _find_error_node(module_node):
    return module_node.body[1].body[0]  # ClassDef -> `run` FunctionDef


_EXPECTED_ERRORS = {
    "kwargs": {
        "versions": ">=2",
        "msg_id": "nb-job-run-unpacking",
        "line": 5,
        "end_line": 5,
        "col_offset": 4,
        "end_col_offset": 11,
        "node": _find_error_node,
        "args": ("**kwargs",),
    },
    "data": {
        "versions": ">=2",
        "msg_id": "nb-job-run-unpacking",
        "line": 5,
        "end_line": 5,
        "col_offset": 4,
        "end_col_offset": 11,
        "node": _find_error_node,
        "args": ("**data",),
    },
    "args": {
        "versions": ">=2",
        "msg_id": "nb-job-run-unpacking",
        "line": 5,
        "end_line": 5,
        "col_offset": 4,
        "end_col_offset": 11,
        "node": _find_error_node,
        "args": ("*args",),
    },
}


class TestJobRunUnpackingChecker(CheckerTestCase):
    """Test job run unpacking checker."""

    CHECKER_CLASS = NautobotJobRunUnpackingChecker

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_error(self, filename, expected_error):
        assert_error_file(self, filename, expected_error)

    @parametrize_good_files(__file__)
    def test_good(self, filename):
        assert_good_file(self, filename)

    @pytest.mark.skipif(is_version_compatible("<2"), reason="Only applicable to Nautobot v2+")
    def test_args_and_kwargs(self):
        """A `run` method with both `*args` and `**kwargs` emits a message for each operator."""
        test_code = (INPUTS_PATH / _CHECKER_DIR / "both_args_and_kwargs.py").read_text(encoding="utf-8")
        module_node = astroid.parse(test_code)
        run_node = _find_error_node(module_node)
        with self.assertAddsMessages(
            MessageTest(
                msg_id="nb-job-run-unpacking",
                node=run_node,
                line=5,
                end_line=5,
                col_offset=4,
                end_col_offset=11,
                args=("*args",),
            ),
            MessageTest(
                msg_id="nb-job-run-unpacking",
                node=run_node,
                line=5,
                end_line=5,
                col_offset=4,
                end_col_offset=11,
                args=("**kwargs",),
            ),
        ):
            self.walk(module_node)
