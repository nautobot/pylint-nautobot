"""Check for imports whose paths have changed in 2.0."""

from astroid import ClassDef
from pylint.checkers import BaseChecker

from .utils import find_ancestor
from .utils import get_model_name
from .utils import is_version_compatible

_ANCESTORS = {
    "nautobot.extras.filters.NautobotFilterSet": ">=2",
}

_VERSION_COMPATIBLE_ANCESTORS = [key for key, value in _ANCESTORS.items() if is_version_compatible(value)]


class NautobotSubClassNameChecker(BaseChecker):
    """Ensure subclass name is <model class name><ancestor class type>.

    This can typically be done via <ancestor class name>.replace("Nautobot", <model class name>)
    """

    version_specifier = ">1,<3"

    name = "nautobot-sub-class-name"
    msgs = {
        "E4242": (
            "Sub-class name should be %s.",
            "nb-sub-class-name",
            "All classes should have a sub-class name that is <model class name><ancestor class type>.",
        )
    }

    def visit_classdef(self, node: ClassDef):
        """Visit class definitions."""
        ancestor = find_ancestor(node, _VERSION_COMPATIBLE_ANCESTORS)
        if not ancestor:
            return

        class_name = node.name
        model_name = get_model_name(ancestor, node)
        expected_name = ancestor.split(".")[-1].replace("Nautobot", model_name)
        if expected_name != class_name:
            self.add_message("nb-sub-class-name", node=node, args=(expected_name,))
