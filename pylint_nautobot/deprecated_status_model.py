"""Check for deprecated StatusModel usage and encourage the usage of StatusField instead."""

from pylint.checkers import BaseChecker

from .utils import find_ancestor


class NautobotDeprecatedStatusModelChecker(BaseChecker):
    """Discourage the usage of deprecated StatusModel and encourage the usage of StatusField."""

    version_specifier = ">=2,<4"

    name = "nautobot-deprecated-status-model"
    msgs = {
        "E4292": (
            "Inherits from the deprecated StatusModel instead of declaring status on the model explicitly with StatusField",
            "nb-status-field-instead-of-status-model",
            "Reference: https://docs.nautobot.com/projects/core/en/stable/user-guide/platform-functionality/status/#status-internals",
        ),
    }

    def visit_classdef(self, node):
        """Visit class definitions."""
        if find_ancestor(node, ["nautobot.extras.models.statuses.StatusModel"]):
            self.add_message("nb-status-field-instead-of-status-model", node=node)
