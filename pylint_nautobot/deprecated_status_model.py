"""Check for deprecated StatusModel usage and encourage the usage of StatusField instead."""
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class NautobotDeprecatedStatusModelChecker(BaseChecker):
    """Discourage the usage of deprecated StatusModel and encourage the usage of StatusField."""

    __implements__ = IAstroidChecker

    version_specifier = ">=2,<3"

    name = "nautobot-deprecated-status-model"
    msgs = {
        "E4292": (
            "Inherits from the deprecated StatusModel instead of declaring status on the model explicitly with StatusField",
            "nb-status-field-instead-of-status-model",
            # TBD: Link is not accessible
            "https://docs.nautobot.com/projects/core/en/next/models/extras/status/#status-internals",
        ),
    }

    def visit_classdef(self, node):
        ancestor_class_types = [ancestor.qname() for ancestor in node.ancestors()]
        if "nautobot.extras.models.statuses.StatusModel" in ancestor_class_types:
            self.add_message("nb-status-field-instead-of-status-model", node=node)
