"""Check for usage of models that were replaced in 2.0."""
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class NautobotReplacedModelsImportChecker(BaseChecker):
    """Visit 'import from' statements to find usage of models that have been replaced in 2.0."""

    __implements__ = IAstroidChecker

    version_specifier = ">=2,<3"

    name = "nautobot-replaced-models"
    msgs = {
        "E4211": (
            "Imports a model that has been replaced (dcim.DeviceRole -> extras.Role).",
            "nb-replaced-device-role",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#generic-role-model",
        ),
        "E4212": (
            "Imports a model that has been replaced (dcim.RackRole -> extras.Role).",
            "nb-replaced-rack-role",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#generic-role-model",
        ),
        "E4213": (
            "Imports a model that has been replaced (ipam.Role -> extras.Role).",
            "nb-replaced-ipam-role",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#generic-role-model",
        ),
        "E4214": (
            "Imports a model that has been replaced (dcim.Region -> dcim.Location).",
            "nb-replaced-region",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#site-and-region-models",
        ),
        "E4215": (
            "Imports a model that has been replaced (dcim.Site -> dcim.Location).",
            "nb-replaced-site",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#site-and-region-models",
        ),
        "E4216": (
            "Imports a model that has been replaced (ipam.Aggregate -> ipam.Prefix).",
            "nb-replaced-aggregate",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#aggregate-migrated-to-prefix",
        ),
    }

    def visit_importfrom(self, node):
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
