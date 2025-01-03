"""Check for CharField's or TextField's on models where null=True and blank=True."""

from astroid import Assign, Call, ClassDef
from pylint.checkers import BaseChecker

from pylint_nautobot.constants import MSGS


class NautobotStringFieldBlankNull(BaseChecker):
    """Visit classes to find class children on models who are CharField's or TextField's and check whether they are configured well."""

    version_specifier = ">=1,<3"

    name = "nautobot-string-field-blank-null"
    msgs = {
        **MSGS.E4261,
    }

    def visit_classdef(self, node: ClassDef):
        """Visit class definitions."""
        # We only care about models
        ancestors = [ancestor.qname() for ancestor in node.ancestors()]
        if "django.db.models.base.Model" not in ancestors:
            return

        for child_node in node.get_children():
            blank = False
            null = False
            # We are only interested in assignments
            if not isinstance(child_node, Assign):
                continue
            # We are only interested in assignments to a call
            if not isinstance(child_node.value, Call):
                continue
            # Encountered values: "CharField" or "models.CharField"
            # because they can be ast Name or Attribute nodes
            child_node_name = child_node.value.func.as_string().split(".")[-1]
            # We are only interested in calls to these two models
            if child_node_name not in ("TextField", "CharField"):
                continue
            for keyword in child_node.value.keywords:
                if keyword.arg == "blank" and keyword.value.value is True:
                    blank = True
                if keyword.arg == "null" and keyword.value.value is True:
                    null = True
            if null and blank:
                self.add_message(msgid="nb-string-field-blank-null", node=child_node)
