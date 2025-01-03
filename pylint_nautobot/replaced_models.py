"""Check for usage of models that were replaced in 2.0."""

from pylint.checkers import BaseChecker

from pylint_nautobot.constants import MSGS


class NautobotReplacedModelsImportChecker(BaseChecker):
    """Visit 'import from' statements to find usage of models that have been replaced in 2.0."""

    version_specifier = ">=2,<3"

    name = "nautobot-replaced-models"
    msgs = {
        **MSGS.E4211,
        **MSGS.E4212,
        **MSGS.E4213,
        **MSGS.E4214,
        **MSGS.E4215,
        **MSGS.E4216,
    }

    def visit_importfrom(self, node):
        """Visit 'import from' statements."""
        if node.modname == "nautobot.dcim.models":
            for name, _ in node.names:
                if name == "DeviceRole":
                    self.add_message("nb-replaced-device-role", node=node)
                elif name == "RackRole":
                    self.add_message("nb-replaced-rack-role", node=node)
                elif name == "Region":
                    self.add_message("nb-replaced-region", node=node)
                elif name == "Site":
                    self.add_message("nb-replaced-site", node=node)
        if node.modname == "nautobot.ipam.models":
            for name, _ in node.names:
                if name == "Role":
                    self.add_message("nb-replaced-ipam-role", node=node)
                elif name == "Aggregate":
                    self.add_message("nb-replaced-aggregate", node=node)
