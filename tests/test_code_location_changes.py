# pylint: disable=duplicate-code
"""Tests for code location changes checker."""
import astroid
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest
from pytest import mark

from pylint_nautobot.code_location_changes import NautobotCodeLocationChangesChecker


class TestCodeLocationChangesChecker(CheckerTestCase):
    """Test model label construction checker."""

    CHECKER_CLASS = NautobotCodeLocationChangesChecker

    @mark.parametrize(
        ("test_code", "expected_args"),
        (
            ("import nautobot.core.fields", ("nautobot.core.fields", "nautobot.core.models.fields")),
            ("from nautobot.core.fields import anything", ("nautobot.core.fields", "nautobot.core.models.fields")),
        ),
    )
    def test_code_location_changed(self, test_code, expected_args):
        module_node = astroid.parse(test_code)
        import_node = module_node.body[0]  # type: ignore
        with self.assertAddsMessages(
            MessageTest(
                msg_id="nb-code-location-changed",
                node=import_node,
                line=1,
                end_line=1,
                col_offset=0,
                end_col_offset=len(test_code),
                args=expected_args,
            ),
        ):
            self.walk(module_node)

    @mark.parametrize(
        ("test_code", "expected_args"),
        (
            (
                "from nautobot.core.api.utils import TreeModelSerializerMixin",
                ("TreeModelSerializerMixin", "nautobot.core.api.utils", "nautobot.core.api.serializers"),
            ),
            (
                "from nautobot.utilities.utils import csv_format",
                ("csv_format", "nautobot.utilities.utils", "nautobot.core.views.utils"),
            ),
        ),
    )
    def test_code_location_changed_object(self, test_code, expected_args):
        module_node = astroid.parse(test_code)
        import_node = module_node.body[0]  # type: ignore
        with self.assertAddsMessages(
            MessageTest(
                msg_id="nb-code-location-changed-object",
                node=import_node,
                line=1,
                end_line=1,
                col_offset=0,
                end_col_offset=len(test_code),
                args=expected_args,
            ),
        ):
            self.walk(module_node)

    @mark.parametrize(
        "test_code",
        (
            "from nautobot.core.api.utils import anything",
            "import nautobot",
            "import nautobot.core.api.serializers",
            "import nautobot.core.api.utils",
            "from nautobot.utilities.utils import anything",
        ),
    )
    def test_no_issues(self, test_code):
        module_node = astroid.parse(test_code)
        with self.assertNoMessages():
            self.walk(module_node)
