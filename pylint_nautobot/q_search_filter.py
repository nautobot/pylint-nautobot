"""Check for use of SearchFilter on NautobotFilterSets instead of custom `q` search functions."""

from astroid import Assign, AssignName, ClassDef
from pylint.checkers import BaseChecker

from .utils import is_version_compatible

_META_CLASSES = {
    "nautobot.extras.filters.NautobotFilterSet": ">1",
    "nautobot.apps.filters.NautobotFilterSet": ">1",
}


class NautobotUseSearchFilterChecker(BaseChecker):
    """Visit NautobotFilterSet subclasses and check for use of `q = SearchFilter`, instead of `q = django_filters.CharField`."""

    version_specifier = ">=2,<3"

    name = "nautobot-use-search-filter"
    msgs = {
        "C4272": (
            "Use `q = SearchFilter` instead of django_filters.CharField and the custom `search` function.",
            "nb-use-search-filter",
            "Nautobot provides a `SearchFilter` class that uses MappedPredicates to provide a more flexible search experience. "
            "This should be used in place of `django_filters.CharFilter` and no longer requires the custom `search` function.",
        ),
    }

    def __init__(self, *args, **kwargs):
        """Initialize the checker."""
        super().__init__(*args, **kwargs)

        self.meta_classes = [
            key for key, specifier_set in _META_CLASSES.items() if is_version_compatible(specifier_set)
        ]

    def visit_classdef(self, node: ClassDef):
        """Visit class definitions."""
        if all(
            ancestor.qname() not in self.meta_classes
            for ancestor in node.ancestors()
        ):
            return

        for child_node in node.get_children():
            if isinstance(child_node, Assign) and any(isinstance(target, AssignName) and target.name == "q" for target in child_node.targets):
                child_node_name = child_node.value.func.as_string().split(".")[-1]
                if child_node_name != "SearchFilter":
                    self.add_message("nb-use-search-filter", node=child_node)
