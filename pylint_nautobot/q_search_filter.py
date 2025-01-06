"""Check for use of SearchFilter on NautobotFilterSets instead of custom `q` search functions."""

from astroid import Assign, AssignName, ClassDef, FunctionDef
from pylint.checkers import BaseChecker

from pylint_nautobot.constants import MESSAGES


class NautobotUseSearchFilterChecker(BaseChecker):
    """Visit NautobotFilterSet subclasses and check for use of `q = SearchFilter`, instead of `q = django_filters.CharField`."""

    version_specifier = ">=2,<3"

    name = "nautobot-use-search-filter"
    msgs = {
        **MESSAGES.C4272,
        **MESSAGES.C4273,
        **MESSAGES.C4274,
    }

    def visit_classdef(self, node: ClassDef):
        """Visit class definitions."""
        for ancestor in node.ancestors():
            if ancestor.qname() != "nautobot.extras.filters.NautobotFilterSet":
                return

            for child_node in node.get_children():
                if isinstance(child_node, Assign) and any(
                    isinstance(target, AssignName) and target.name == "q" for target in child_node.targets
                ):
                    child_node_name = child_node.value.func.as_string().split(".")[-1]
                    # The `q` attribute should not be a CharFilter, instead it should be a SearchFilter
                    if child_node_name == "CharFilter":
                        self.add_message("nb-no-char-filter-q", node=child_node)
                    # Warn but allow override if the `q` attribute is not a SearchFilter as this could be inherited from the SearchFilter
                    elif child_node_name != "SearchFilter":
                        self.add_message("nb-use-search-filter", node=child_node)
                if isinstance(child_node, FunctionDef) and child_node.name == "search":
                    self.add_message("nb-no-search-function", node=child_node)
