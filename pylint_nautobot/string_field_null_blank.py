"""Check for CharField's or TextField's on models where null=True and blank=True."""
from astroid import ClassDef, Assign, Call
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class NautobotStringFieldBlankNull(BaseChecker):
    """Visit classes to find class children on models who are CharField's or TextField's and check whether they are configured well."""

    __implements__ = IAstroidChecker

    version_specifier = ">=1,<3"

    name = "nautobot-string-field-blank-null"
    msgs = {
        "E4261": (
            "Uses bad parameter combination for TextField/CharField.",
            "nb-string-field-blank-null",
            "Don't use blank=true and null=true on TextField or CharField",
        ),
    }

    def visit_classdef(self, node: ClassDef):
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
            for keyword in child_node.value.keywords:
                if keyword.arg == "blank" and keyword.value.value is True:
                    blank = True
                if keyword.arg == "null" and keyword.value.value is True:
                    null = True
            if null and blank:
                self.add_message(msgid="nb-string-field-blank-null", node=node)
