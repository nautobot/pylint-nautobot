"""Check for incorrect base classes."""
from typing import NamedTuple

from astroid import Assign
from astroid import ClassDef
from astroid import Const
from pylint.checkers import BaseChecker

from .utils import is_version_compatible


def is_abstract(node: ClassDef) -> bool:
    """Given a node, returns whether it is an abstract base model."""
    for child_node in node.get_children():
        if not (isinstance(child_node, ClassDef) and child_node.name == "Meta"):
            continue

        for meta_child in child_node.get_children():
            if (
                not isinstance(meta_child, Assign)
                or not meta_child.targets[0].name == "abstract"  # type: ignore
                or not isinstance(meta_child.value, Const)
            ):
                continue
            # At this point we know we are dealing with an assignment to a constant for the 'abstract' field on the
            # 'Meta' class. Therefore, we can assume the value of that to be whether the node is an abstract base model
            # or not.
            return meta_child.value.value

    return False


_CLASS_MAPPING = (
    {
        "incorrect": "django_filters.filters.FilterSet",
        "correct": "django_filters.filters.BaseFilterSet",
    },
    {
        "incorrect": "django.db.models.base.Model",
        "correct": "nautobot.core.models.BaseModel",
    },
    {
        "versions": "<2.0",
        "incorrect": "django.forms.forms.Form",
        "correct": "nautobot.utilities.forms.forms.BootstrapMixin",
    },
    {
        "versions": ">=2.0",
        "incorrect": "django.forms.forms.Form",
        "correct": "nautobot.core.forms.forms.BootstrapMixin",
    },
    {
        "versions": ">=2.0",
        "incorrect": "django.forms.ModelForm",
        "correct": "nautobot.apps.forms.NautobotModelForm",
    },
    {
        "versions": ">=2.0",
        "incorrect": "nautobot.extras.plugins.PluginConfig",
        "correct": "nautobot.apps.NautobotAppConfig",
    },
)


class _Mapping(NamedTuple):
    incorrect: str
    correct: str


_COMPATIBLE_MAPPING = (
    _Mapping(item["incorrect"], item["correct"])
    for item in _CLASS_MAPPING
    if is_version_compatible(item.get("versions", ""))
)


class NautobotIncorrectBaseClassChecker(BaseChecker):
    """Check that all X inherits from Y.

    Example: Every model that you define in the Nautobot ecosystem should inherit from 'nautobot.core.models.BaseModel'.
    """

    version_specifier = ">=1,<3"

    # Maps a non-Nautobot-specific base class to a Nautobot-specific base class which has to be in the class hierarchy
    # for every class that has the base class in its hierarchy.
    name = "nautobot-incorrect-base-class"
    msgs = {
        "E4242": (
            "Uses incorrect base classes (%s -> %s).",
            "nb-incorrect-base-class",
            "All classes should inherit from the correct base classes.",
        )
    }

    def visit_classdef(self, node: ClassDef):
        """Visit class definitions."""
        if is_abstract(node):
            return

        # Skip mixin classes
        if "Mixin" in node.name:
            return

        ancestor_class_types = [ancestor.qname() for ancestor in node.ancestors()]
        for mapping in _COMPATIBLE_MAPPING:
            if mapping.incorrect in ancestor_class_types and mapping.correct not in ancestor_class_types:
                self.add_message(msgid="nb-incorrect-base-class", node=node, args=(mapping.incorrect, mapping.correct))
                return
