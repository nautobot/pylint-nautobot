"""Check for deprecated StatusModel usage and encourage the usage of StatusField instead."""

from pylint.checkers import BaseChecker

from pylint_nautobot.constants import MSGS


class NautobotDeprecatedStatusModelChecker(BaseChecker):
    """Discourage the usage of deprecated StatusModel and encourage the usage of StatusField."""

    version_specifier = ">=2,<3"

    name = "nautobot-deprecated-status-model"
    msgs = {
        **MSGS.E4292,
    }

    def visit_classdef(self, node):
        """Visit class definitions."""
        ancestor_class_types = [ancestor.qname() for ancestor in node.ancestors()]
        if "nautobot.extras.models.statuses.StatusModel" in ancestor_class_types:
            self.add_message("nb-status-field-instead-of-status-model", node=node)
