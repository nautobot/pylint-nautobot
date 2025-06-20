"""Warn about double underscore filter fields in NautobotFilterSet subclasses."""

from astroid import Assign, AssignName, ClassDef
from pylint.checkers import BaseChecker


class NautobotDunderFilterFieldChecker(BaseChecker):
    """Visit NautobotFilterSet subclasses and check for use of __ in the field name."""

    version_specifier = ">=2,<4"

    name = "nautobot-warn-dunder-filter-field"
    msgs = {
        "W4275": (
            "Avoid using double underscores in filter field names.",
            "nb-warn-dunder-filter-field",
            "Double underscores in filter field names are reserved for nested lookups and can cause unexpected behavior. "
            "Use single underscores instead.",
        ),
    }

    def visit_classdef(self, node: ClassDef):
        """Visit class definitions."""
        ancestors = [ancestor.qname() for ancestor in node.ancestors()]
        if "nautobot.extras.filters.NautobotFilterSet" not in ancestors:
            return

        for child_node in node.get_children():
            if isinstance(child_node, Assign) and any(
                isinstance(target, AssignName) and "__" in target.name for target in child_node.targets
            ):
                self.add_message("nb-warn-dunder-filter-field", node=child_node)
