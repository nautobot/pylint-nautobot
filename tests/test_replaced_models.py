# pylint: disable=duplicate-code
"""Tests for replaced models checker."""
import astroid
from pylint.testutils import CheckerTestCase
from pylint.testutils import MessageTest
from pytest import mark

from pylint_nautobot.replaced_models import NautobotReplacedModelsImportChecker


class TestReplacedModelsImportChecker(CheckerTestCase):
    """Test model label construction checker."""

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
        module_node = astroid.parse(test_code)
        import_node = module_node.body[0]  # type: ignore
        with self.assertAddsMessages(
            MessageTest(
                msg_id=msg_id,
                node=import_node,
                line=1,
                end_line=1,
                col_offset=0,
                end_col_offset=len(test_code),
            ),
        ):
            self.walk(module_node)

    @mark.parametrize(
        "test_code",
        (
            "from nautobot.dcim.models import Device",
            "from nautobot.ipam.models import IpAddress",
        ),
    )
    def test_no_issues(self, test_code):
        module_node = astroid.parse(test_code)
        with self.assertNoMessages():
            self.walk(module_node)
