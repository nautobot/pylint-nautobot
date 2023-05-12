"""Check for imports whose paths have changed in 2.0."""
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint_nautobot.utils import MAP_CODE_LOCATION_CHANGES


class NautobotCodeLocationChangesChecker(BaseChecker):
    """Visit 'import from' statements to find import locations that have moved in 2.0."""

    __implements__ = IAstroidChecker

    version_specifier = ">=2,<3"

    name = "nautobot-code-location-changes"
    msgs = {
        "E4251": (
            "Import location has changed (%s -> %s).",
            "nb-code-location-changed",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#python-code-location-changes",
        ),
        "E4252": (
            "Import location has changed for %s (%s -> %s).",
            "nb-code-location-changed-object",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#python-code-location-changes",
        ),
    }

    def visit_importfrom(self, node):
        """Verifies whether entire module imports or individual objects have moved."""
        if node.modname in MAP_CODE_LOCATION_CHANGES:
            import_changed_to = MAP_CODE_LOCATION_CHANGES[node.modname]
            if "(all)" in import_changed_to:
                # from nautobot.utilities.templatetags import ...
                self.add_message(
                    "nb-code-location-changed",
                    node=node,
                    args=(node.modname, import_changed_to["(all)"]),
                )
            for imported_name in (n for n, _ in node.names):
                # from nautobot.core.api.utils import TreeModelSerializerMixin
                if imported_name in import_changed_to:
                    self.add_message(
                        "nb-code-location-changed-object",
                        node=node,
                        args=(imported_name, node.modname, import_changed_to[imported_name]),
                    )
