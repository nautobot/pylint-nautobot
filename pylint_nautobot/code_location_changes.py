"""Check for imports whose paths have changed in 2.0."""

from pylint.checkers import BaseChecker

from pylint_nautobot.utils import MAP_CODE_LOCATION_CHANGES


class NautobotCodeLocationChangesChecker(BaseChecker):
    """Visit 'import from' statements to find import locations that have moved in 2.0."""

    version_specifier = ">=2,<4"

    name = "nautobot-code-location-changes"
    msgs = {
        "E4251": (
            "Import location has changed (%s -> %s).",
            "nb-code-location-changed",
            "Reference: https://docs.nautobot.com/projects/core/en/stable/development/apps/migration/code-updates/",
        ),
        "E4252": (
            "Import location has changed for %s (%s -> %s).",
            "nb-code-location-changed-object",
            "Reference: https://docs.nautobot.com/projects/core/en/stable/development/apps/migration/code-updates/",
        ),
    }

    def visit_import(self, node):
        """Verifies whether entire module imports have moved.

        e.g.: `import nautobot.core.fields` is invalid.
        """
        for name, _ in node.names:
            if name in MAP_CODE_LOCATION_CHANGES:
                import_changed_to = MAP_CODE_LOCATION_CHANGES[name]
                if "(all)" in import_changed_to:
                    self.add_message(
                        "nb-code-location-changed",
                        node=node,
                        args=(name, import_changed_to["(all)"]),
                    )

    def visit_importfrom(self, node):
        """Verifies whether entire module imports or individual objects have moved.

        e.g. `from nautobot.utilities import templatetags` is invalid.
        """
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
