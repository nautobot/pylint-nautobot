"""Check for CharField's or TextField's on models where null=True and blank=True."""

from astroid import Assign
from astroid import AssignName
from astroid import ClassDef
from astroid import Const
from pylint.checkers import BaseChecker

from .utils import is_version_compatible

_META_CLASSES = {
    "nautobot.core.api.serializers.NautobotModelSerializer.Meta": ">1",
    "nautobot.core.tables.BaseTable.Meta": ">=2",
    "nautobot.extras.filters.NautobotFilterSet.Meta": ">1",
    "nautobot.extras.forms.NautobotModelForm.Meta": ">1",
    "nautobot.utilities.tables.BaseTable.Meta": ">1,<2",
}


class NautobotUseFieldsAllChecker(BaseChecker):
    """Visit Meta subclasses and check for use of `fields = "__all__"`, instead of `fields = ["field1", ...]`."""

    version_specifier = ">=1,<3"

    name = "nautobot-use-fields-all"
    msgs = {
        "E4271": (
            "Use `fields = '__all__'` instead of specifying each field individually.",
            "nb-use-fields-all",
            "Defining `fields = '__all__'` in a model serializer's Meta class is a Django convention that automatically "
            "includes all fields from the associated model. This approach is more maintainable because it avoids having "
            "to explicitly list each field, reducing the risk of errors and inconsistencies when the model is updated.",
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
        if not any(ancestor.qname() in self.meta_classes for ancestor in node.ancestors()):
            return

        for child_node in node.get_children():
            if isinstance(child_node, Assign):
                if any(isinstance(target, AssignName) and target.name == "fields" for target in child_node.targets):
                    value = child_node.value
                    if not (isinstance(value, Const) and value.value == "__all__"):
                        self.add_message("nb-use-fields-all", node=value)
