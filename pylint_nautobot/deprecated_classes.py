"""Check for deprecated class usage and encourage the usage of the replacement class instead."""

from importlib_resources import files
from pylint.checkers import BaseChecker
from yaml import safe_load

from pylint_nautobot.utils import find_ancestor


def load_v3_code_removals() -> dict[str, str]:
    """Load the v3 code removals data."""
    with open(
        files("pylint_nautobot") / "data" / "v3" / "v3-code-removals.yaml",
        encoding="utf-8",
    ) as rules:
        removals = safe_load(rules)
    return {removal["Removed"]: removal["Replacement"] for removal in removals}


class NautobotDeprecatedClassChecker(BaseChecker):
    """Discourage the usage of deprecated class and encourage the usage of the replacement class."""

    version_specifier = ">=2,<4"

    name = "nautobot-deprecated-class"
    msgs = {
        "E4293": (
            "Class %s is deprecated. Use %s instead.",
            "nb-deprecated-class",
            "Reference: https://docs.nautobot.com/projects/core/en/stable/release-notes/version-3.0/#removed-python-code",
        ),
    }

    def visit_classdef(self, node):
        """Visit class definitions."""
        v3_removals = load_v3_code_removals()
        for removed, replacement in v3_removals.items():
            if find_ancestor(node, [removed]):
                self.add_message("nb-deprecated-class", node=node, args=(removed, replacement))
