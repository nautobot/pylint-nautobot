"""Tests for code location changes checker."""
from pylint.testutils import CheckerTestCase
from pytest import mark

from pylint_nautobot.code_location_changes import NautobotCodeLocationChangesChecker

from .utils import assert_no_message, assert_import_error


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
        assert_import_error(self, "nb-code-location-changed", test_code, expected_args)

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
        assert_import_error(self, "nb-code-location-changed-object", test_code, expected_args)

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
        assert_no_message(self, test_code)
