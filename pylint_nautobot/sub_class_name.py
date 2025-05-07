"""Check for imports whose paths have changed in 2.0."""

from typing import NamedTuple

from astroid import ClassDef
from pylint.checkers import BaseChecker

from .utils import find_ancestor, find_model_name, is_abstract_class, is_version_compatible, trim_first_pascal_word

_ANCESTORS = (
    {
        "versions": ">=2",
        "ancestor": "nautobot.extras.filters.NautobotFilterSet",
    },
    {
        "versions": "<1",  # Disabled, unable to find a model inside the class
        "ancestor": "nautobot.extras.forms.base.BulkEditForm",
    },
    {
        "versions": ">=2",
        "ancestor": "nautobot.extras.forms.base.NautobotFilterForm",
    },
    {
        "versions": ">=2",
        "ancestor": "nautobot.extras.forms.base.NautobotModelForm",
        "suffix": "Form",
    },
    {
        "versions": ">=2",
        "ancestor": "nautobot.core.api.serializers.NautobotModelSerializer",
        "suffix": "Serializer",
    },
    {
        "versions": ">=2",
        "ancestor": "nautobot.core.views.viewsets.NautobotUIViewSet",
    },
    {
        "versions": ">=2",
        "ancestor": "nautobot.core.tables.BaseTable",
    },
)


class _Ancestor(NamedTuple):
    ancestor: str
    suffix: str


def _get_ancestor(item: dict) -> _Ancestor:
    ancestor = item["ancestor"]
    return _Ancestor(ancestor, item.get("suffix", trim_first_pascal_word(ancestor.split(".")[-1])))


class NautobotSubClassNameChecker(BaseChecker):
    """Ensure subclass name is <model class name><ancestor class type>.

    This can typically be done via <ancestor class name>.replace("Nautobot", <model class name>)
    """

    version_specifier = ">=2,<4"

    name = "nautobot-sub-class-name"
    msgs = {
        "E4281": (
            "Sub-class name should be %s.",
            "nb-sub-class-name",
            "All classes should have a sub-class name that is <model class name><ancestor class type>.",
        ),
        "I4282": (
            "Model was not found in the class.",
            "nb-no-model-found",
            "Model was not found in the class.",
        ),
    }

    def __init__(self, *args, **kwargs):
        """Initialize the checker."""
        super().__init__(*args, **kwargs)

        self.ancestors = tuple(_get_ancestor(item) for item in _ANCESTORS if is_version_compatible(item["versions"]))

    def visit_classdef(self, node: ClassDef):
        """Visit class definitions."""
        if is_abstract_class(node):
            return

        ancestor = find_ancestor(node, self.ancestors, lambda item: item.ancestor)
        if not ancestor:
            return

        model_name = find_model_name(node)
        if model_name:
            expected_name = model_name + ancestor.suffix
            if expected_name != node.name:
                self.add_message("nb-sub-class-name", node=node, args=(expected_name,))
        else:
            self.add_message("nb-no-model-found", node=node)
