"""Check for CharField's or TextField's on models where null=True and blank=True."""

from astroid import Assign, Call, ClassDef
from pylint.checkers import BaseChecker


class NautobotStringFieldBlankNull(BaseChecker):
    """Visit classes to find class children on models who are CharField's or TextField's and check whether they are configured well."""

    version_specifier = ">=1,<4"

    name = "nautobot-string-field-blank-null"
    msgs = {
        "E4261": (
            "Uses bad parameter combination for TextField/CharField.",
            "nb-string-field-blank-null",
            'Don\'t use blank=true and null=true on TextField or CharField. \
             It avoids confusion between a value of None and a value of ""\
             potentially having different meanings.',
        ),
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
