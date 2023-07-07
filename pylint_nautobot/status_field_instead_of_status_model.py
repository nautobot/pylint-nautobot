"""Check for deprecated StatusModel usage and encourage the usage of StatusField instead."""
from pylint.checkers import BaseChecker


class NautobotDeprecatedStatusModelChecker(BaseChecker):
    """Discourage the usage of deprecated StatusModel and encourage the usage of StatusField."""

    version_specifier = ">=2,<3"

    name = "nautobot-status-field-instead-of-status-model"
    msgs = {
        "E4292": (
            "Inherits from the deprecated StatusModel instead of declaring status on the model explicitly with StatusField",
            "nb-status-field-instead-of-status-model",
            "https://docs.nautobot.com/projects/core/en/next/models/extras/status/#status-internals",
        ),
    }

    def visit_classdef(self, node):
        ancestor_class_types = [ancestor.qname() for ancestor in node.ancestors()]
        if "nautobot.extras.models.statuses.StatusModel" in ancestor_class_types:
            self.add_message("nb-status-field-instead-of-status-model", node=node)
