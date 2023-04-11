import astroid

from pylint_nautobot import NautobotReplacedModelsImportChecker


def test_replaced_models(mocker):
    node = astroid.extract_node(
        """
        from nautobot.dcim.models import DeviceRole
    """
    )
    linter = mocker.MagicMock()
    checker = NautobotReplacedModelsImportChecker(linter=linter)
    checker.visit_importfrom(node)
    linter.add_message.assert_called_with(
        "nb-replaced-device-role", None, node, None, None, None, None, None
    )
