"""Check for use of SearchFilter on NautobotFilterSets instead of custom `q` search functions."""

from astroid import Assign, AssignName, ClassDef, FunctionDef
from pylint.checkers import BaseChecker


class NautobotUseSearchFilterChecker(BaseChecker):
    """Visit NautobotFilterSet subclasses and check for use of `q = SearchFilter`, instead of `q = django_filters.CharField`."""

    version_specifier = ">=2,<4"

    name = "nautobot-use-search-filter"
    msgs = {
        "C4272": (
            "Use `q = SearchFilter` instead of django_filters.CharFilter and the custom `search` function.",
            "nb-no-char-filter-q",
            "Nautobot provides a `SearchFilter` class that uses MappedPredicates to provide a more flexible search experience. "
            "This should be used in place of `django_filters.CharFilter` and no longer requires the custom `search` function.",
        ),
        "C4273": (
            "Use `q = SearchFilter` instead.",
            "nb-use-search-filter",
            "Nautobot provides a `SearchFilter` class that uses MappedPredicates to provide a more flexible search experience. "
            "This can be disabled if you need to use a custom Filter.",
        ),
        "C4274": (
            "Don't use custom `search` function, use SearchFilter instead.",
            "nb-no-search-function",
            "Nautobot provides a `SearchFilter` class that uses MappedPredicates to provide a more flexible search experience. "
            "This should be used in place of the custom `search` function.",
        ),
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
