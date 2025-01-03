"""Check for CharField's or TextField's on models where null=True and blank=True."""

from astroid import Assign, AssignName, ClassDef, Const
from pylint.checkers import BaseChecker

from pylint_nautobot.constants import MSGS
from pylint_nautobot.utils import find_meta, is_version_compatible

_META_CLASSES = {
    "nautobot.core.api.serializers.NautobotModelSerializer": ">=2",
    "nautobot.extras.filters.NautobotFilterSet": ">1",
    "nautobot.extras.forms.base.NautobotModelForm": ">1",
}


class NautobotUseFieldsAllChecker(BaseChecker):
    """Visit Meta subclasses and check for use of `fields = "__all__"`, instead of `fields = ["field1", ...]`."""

    version_specifier = ">=1,<3"

    name = "nautobot-use-fields-all"
    msgs = {
        **MSGS.E4271,
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

        meta = find_meta(node)
        if not meta:
            return

        for child_node in meta.get_children():
            if isinstance(child_node, Assign):
                if any(isinstance(target, AssignName) and target.name == "fields" for target in child_node.targets):
                    value = child_node.value
                    if not (isinstance(value, Const) and value.value == "__all__"):
                        self.add_message("nb-use-fields-all", node=value)
