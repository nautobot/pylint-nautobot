"""Tests for replaced models checker."""

from pylint.testutils import CheckerTestCase
from pytest import mark

from pylint_nautobot.replaced_models import NautobotReplacedModelsImportChecker

from .utils import assert_import_error, assert_no_message


class TestReplacedModelsImportChecker(CheckerTestCase):
    """Test replaced models import checker."""

    CHECKER_CLASS = NautobotReplacedModelsImportChecker

    @mark.parametrize(
        ("msg_id", "test_code"),
        (
            ("nb-replaced-aggregate", "from nautobot.ipam.models import Aggregate"),
            ("nb-replaced-device-role", "from nautobot.dcim.models import DeviceRole"),
            ("nb-replaced-ipam-role", "from nautobot.ipam.models import Role"),
            ("nb-replaced-rack-role", "from nautobot.dcim.models import RackRole"),
            ("nb-replaced-region", "from nautobot.dcim.models import Region"),
            ("nb-replaced-site", "from nautobot.dcim.models import Site"),
        ),
    )
    def test_code_location_changed(self, msg_id, test_code):
        assert_import_error(self, msg_id, test_code)

    @mark.parametrize(
        "test_code",
        (
            "from nautobot.dcim.models import Device",
            "from nautobot.ipam.models import IPAddress",
        ),
    )
    def test_no_issues(self, test_code):
        assert_no_message(self, test_code)
