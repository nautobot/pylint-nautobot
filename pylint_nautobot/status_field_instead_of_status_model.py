"""Check for deprecated StatusModel usage and encourage the usage of StatusField instead."""
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class NautobotDeprecatedStatusModelChecker(BaseChecker):
    """Discourage the usage of deprecated StatusModel and encourage the usage of StatusField."""

    __implements__ = IAstroidChecker

    version_specifier = ">=2,<3"

    name = "nautobot-status-field-instead-of-status-model"
    msgs = {
        "E4292": (
            "Declare status on the model explicitly with a StatusField, as StatusModel is deprecated",
            "nb-status-field-instead-of-status-model",
            "https://docs.nautobot.com/projects/core/en/next/models/extras/status/#status-internals",
        ),
    }

    def visit_classdef(self, node):
        for basename in node.basenames:
            if basename in ["StatusModel", "statuses.StatusModel"]:
                self.add_message("nb-status-field-instead-of-status-model", node=node)
