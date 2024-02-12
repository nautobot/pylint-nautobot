"""Check for imports whose paths have changed in 2.0."""

from pylint.checkers import BaseChecker

from .utils import is_abstract_class
from .utils import is_version_compatible


class NautobotIncorrectBaseClassChecker(BaseChecker):
    """Check that all X inherits from Y.

    Example: Every model that you define in the Nautobot ecosystem should inherit from 'nautobot.core.models.BaseModel'.
    """

    version_specifier = ">=1,<3"

    # Maps a non-Nautobot-specific base class to a Nautobot-specific base class which has to be in the class hierarchy
    # for every class that has the base class in its hierarchy.
    external_to_nautobot_class_mapping = [
        ("django_filters.filters.FilterSet", "django_filters.filters.BaseFilterSet"),
        ("django.db.models.base.Model", "nautobot.core.models.BaseModel"),
        (
            "django.forms.forms.Form",
            (
                "nautobot.core.forms.forms.BootstrapMixin"
                if is_version_compatible(">=2")
                else "nautobot.utilities.forms.forms.BootstrapMixin"
            ),
        ),
    ]

    name = "nautobot-incorrect-base-class"
    msgs = {
        "E4242": (
            "Uses incorrect base classes (%s -> %s).",
            "nb-incorrect-base-class",
            "All classes should inherit from the correct base classes.",
        )
    }

    def visit_classdef(self, node):
        """Visit class definitions."""
        if is_abstract_class(node):
            return

        # Skip mixin classes
        if "Mixin" in node.name:
            return

        ancestor_class_types = [ancestor.qname() for ancestor in node.ancestors()]
        for base_class, nautobot_base_class in self.external_to_nautobot_class_mapping:
            if base_class in ancestor_class_types and nautobot_base_class not in ancestor_class_types:
                self.add_message(msgid="nb-incorrect-base-class", node=node, args=(base_class, nautobot_base_class))
