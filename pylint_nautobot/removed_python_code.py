"""Check for usage of models that were replaced in 2.0."""

import importlib_resources

import yaml

import astroid

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


with open(
    importlib_resources.files("pylint_nautobot").joinpath("data/v2/v2-removed-code.yaml"), encoding="utf-8"
) as fh:
    V2_REMOVED_CODE = yaml.safe_load(fh)


class NautobotRemovedCodeImportChecker(BaseChecker):
    """Visit 'import from' statements to find usage of models that have been replaced in 2.0."""

    __implements__ = IAstroidChecker

    version_specifier = ">=2,<3"

    name = "nautobot-import-removed-code"
    msgs = {
        "E4411": (
            "Imports code that has been removed (%s).",
            "nb-import-removed-code",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/?h=serialize_object#removed-python-code",
        ),
    }

    def visit_importfrom(self, node: astroid.ImportFrom) -> None:
        """Look for removed code in from ... import ... statements."""
        removed_from_module = V2_REMOVED_CODE.get(node.modname)
        if removed_from_module is not None:
            # if module has been removed, then all imports can be logged
            if removed_from_module[0] == "all":
                # node.names is a list of 2-item tuples of item imported and name it is imported as, e.g. from x import y as z -> [(y, z)]
                for name in node.names:
                    self.add_message("nb-import-removed-code", node=node, args=(f"{node.modname}.{name[0]}",))
                return None

            for name in node.names:
                nautobot_name = name[0]
                if nautobot_name in removed_from_module:
                    self.add_message("nb-import-removed-code", node=node, args=(f"{node.modname}.{nautobot_name}",))

        return None

    def visit_import(self, node: astroid.Import) -> None:
        """Look for removed code in import ... statements."""
        # node.names is a list of 2-item tuples of item imported and name it is imported as, e.g. import x.y as z -> [(x.y, z)]
        for name in node.names:
            nautobot_name = name[0]
            nautobot_object = None
            # Check if importing a module, e.g. import nautobot.dcim.filters
            removed_from_module = V2_REMOVED_CODE.get(nautobot_name)
            # Check if importing an object from a module, e.g. nautobot.dcim.filters.DeviceFilter
            if removed_from_module is None:
                module, nautobot_object = nautobot_name.rsplit(".", 1)
                removed_from_module = V2_REMOVED_CODE.get(module)
            if removed_from_module is None:
                continue
            if removed_from_module[0] == "all":
                self.add_message("nb-import-removed-code", node=node, args=(nautobot_name,))
            elif nautobot_object is not None and nautobot_object in removed_from_module:
                self.add_message("nb-import-removed-code", node=node, args=(nautobot_name,))
