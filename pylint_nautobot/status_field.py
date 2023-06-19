"""Check for usage of StatusModel and recommend StatusField instead."""
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class NautobotStatusFieldChecker(BaseChecker):
    """Check for usage of StatusModel and recommend StatusField instead."""

    __implements__ = IAstroidChecker

    version_specifier = ">=2,<3"

    name = "nautobot-code-location-changes"
    msgs = {
        "E4271": (
            "Use StatusField",
            "nb-status-field",
            "TODO",
        ),
    }

    def visit_classdef(self, node):
        """Verifies that classes don't inherit from StatusModel directly."""
        direct_ancestor_classes = [ancestor.qname() for ancestor in node.ancestors(recurs=False)]
        if "nautobot.extras.models.StatusModel" in direct_ancestor_classes:
            self.add_message(msgid="nb-status-field", node=node)

