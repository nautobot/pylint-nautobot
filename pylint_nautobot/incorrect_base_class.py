"""Check for imports whose paths have changed in 2.0."""
import inspect

from astroid import ClassDef, Assign, Const
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


def to_path(obj):
    """Given an object, return its fully qualified import path."""
    return f"{inspect.getmodule(obj).__name__}.{obj.__name__}"


def is_abstract(node):
    """Given a node, returns whether it is an abstract base model."""
    for child_node in node.get_children():
        if not (isinstance(child_node, ClassDef) and child_node.name == "Meta"):
            continue
        for meta_child in child_node.get_children():
            if (
                not isinstance(meta_child, Assign)
                or not meta_child.targets[0].name == "abstract"
                or not isinstance(meta_child.value, Const)
            ):
                continue
            # At this point we know we are dealing with an assignment to a constant for the 'abstract' field on the
            # 'Meta' class. Therefore, we can assume the value of that to be whether the node is an abstract base model
            # or not.
            return meta_child.value.value
    return False


class NautobotIncorrectBaseClassChecker(BaseChecker):
    """Check that all X inherits from Y.

    Example: Every model that you define in the Nautobot ecosystem should inherit from 'nautobot.core.models.BaseModel'.
    """

    __implements__ = IAstroidChecker

    version_specifier = ">=1,<3"

    # Maps a non-Nautobot-specific base class to a Nautobot-specific base class which has to be in the class hierarchy
    # for every class that has the base class in its hierarchy.
    external_to_nautobot_class_mapping = [
        ("django_filters.filters.FilterSet", "django_filters.filters.BaseFilterSet"),
        ("django.db.models.base.Model", "nautobot.core.models.BaseModel"),
        ("django.forms.forms.Form", "nautobot.utilities.forms.forms.BootstrapMixin"),
    ]

    name = "nautobot-incorrect-base-class"
    msgs = {
        "E4242": (
            "Uses incorrect base classes.",
            "nb-incorrect-base-class",
            "All classes should inherit from the correct base classes.",
        )
    }

    def visit_classdef(self, node):
        if is_abstract(node):
            return

        # Skip mixin classes
        if "Mixin" in node.name:
            return

        ancestor_class_types = [ancestor.qname() for ancestor in node.ancestors()]
        for base_class, nautobot_base_class in self.external_to_nautobot_class_mapping:
            if base_class in ancestor_class_types and nautobot_base_class not in ancestor_class_types:
                self.add_message(msgid="nb-incorrect-base-class", node=node)
