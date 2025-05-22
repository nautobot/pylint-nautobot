"""Check for incorrect base classes."""

from typing import NamedTuple

from astroid import ClassDef
from pylint.checkers import BaseChecker

from .utils import is_abstract_class, is_version_compatible

# Sorted from most specific to least specific
_CLASS_MAPPING = (
    {
        "versions": ">=2.0",
        "incorrect": "django_filters.filterset.BaseFilterSet",
        "correct": "nautobot.extras.filters.NautobotFilterSet",
        "display": "nautobot.apps.filters.NautobotFilterSet",
    },
    {
        "incorrect": "django.db.models.base.Model",
        "correct": "nautobot.core.models.generics.PrimaryModel",
        "display": "nautobot.apps.models.PrimaryModel",
    },
    {
        "versions": ">=2.0",
        "incorrect": "django.forms.models.BaseModelForm",
        "correct": "nautobot.extras.forms.base.NautobotModelForm",
        "display": "nautobot.apps.forms.NautobotModelForm",
    },
    {
        "versions": "<2.0",
        "incorrect": "django.forms.forms.BaseForm",
        "correct": "nautobot.utilities.forms.forms.BootstrapMixin",
    },
    {
        "versions": ">=2.0",
        "incorrect": "django.forms.forms.BaseForm",
        "correct": "nautobot.core.forms.forms.BootstrapMixin",
        "display": "nautobot.apps.forms.BootstrapMixin",
    },
)


class _Mapping(NamedTuple):
    incorrect: str
    correct: str
    display: str


class NautobotIncorrectBaseClassChecker(BaseChecker):
    """Check that all X inherits from Y.

    Example: Every model that you define in the Nautobot ecosystem should inherit from 'nautobot.core.models.BaseModel'.
    """

    version_specifier = ">=1,<4"

    name = "nautobot-incorrect-base-class"
    msgs = {
        "E4242": (
            "Uses incorrect base classes (%s -> %s).",
            "nb-incorrect-base-class",
            "All classes should inherit from the correct base classes.",
        )
    }

    def __init__(self, *args, **kwargs):
        """Initialize the checker."""
        super().__init__(*args, **kwargs)

        self.mappings = (
            _Mapping(item["incorrect"], item["correct"], item.get("display", item["correct"]))
            for item in _CLASS_MAPPING
            if is_version_compatible(item.get("versions", ""))
        )

    def visit_classdef(self, node: ClassDef):
        """Visit class definitions."""
        if is_abstract_class(node):
            return

        # Skip mixin classes
        if "Mixin" in node.name:
            return

        ancestor_class_types = [ancestor.qname() for ancestor in node.ancestors()]

        for mapping in self.mappings:
            if mapping.incorrect in ancestor_class_types and mapping.correct not in ancestor_class_types:
                self.add_message(msgid="nb-incorrect-base-class", node=node, args=(mapping.incorrect, mapping.display))
                return
