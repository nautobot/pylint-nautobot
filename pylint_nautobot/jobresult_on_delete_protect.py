"""Check for ForeignKey and OneToOneField fields to JobResult that should not use PROTECT for on_delete."""

from astroid import Assign, Attribute, Call, ClassDef, Const, Name, NodeNG
from pylint.checkers import BaseChecker

from .utils import find_ancestor


def _is_jobresult_reference(node: NodeNG) -> bool:
    """Check if a node references JobResult model."""
    if isinstance(node, Const) and isinstance(node.value, str):
        # String reference like "extras.JobResult" or "JobResult"
        return node.value.endswith("JobResult") or node.value == "JobResult"
    if isinstance(node, Name):
        # Direct reference like JobResult
        return node.name == "JobResult"
    if isinstance(node, Attribute):
        # Attribute reference like extras.JobResult or models.JobResult
        return node.attrname == "JobResult"
    return False


def _is_protect(node: NodeNG) -> bool:
    """Check if a node represents PROTECT."""
    if isinstance(node, Name):
        return node.name == "PROTECT"
    if isinstance(node, Attribute):
        # Could be models.PROTECT or django.db.models.PROTECT
        return node.attrname == "PROTECT"
    return False


class NautobotJobResultOnDeleteProtectChecker(BaseChecker):
    """Check for ForeignKey and OneToOneField fields to JobResult that should not use PROTECT for on_delete."""

    version_specifier = ">=1,<4"

    name = "nautobot-jobresult-on-delete-protect"
    msgs = {
        "E4294": (
            "Avoid using PROTECT for on_delete on ForeignKey and OneToOneField fields to JobResult.",
            "nb-jobresult-on-delete-protect",
            "Foreign keys and one-to-one fields to JobResult should consider using SET_NULL or CASCADE for on_delete, not PROTECT. "
            "Using PROTECT for on_delete will prevent the JobResult from being cleaned up when using the Nautobot LogsCleanup job.",
        ),
    }

    def visit_classdef(self, node: ClassDef):  # pylint: disable=too-many-branches  # noqa: PLR0912
        """Visit class definitions."""
        # We only care about models
        if not find_ancestor(node, ["django.db.models.base.Model"]):
            return

        for child_node in node.get_children():
            # We are only interested in assignments
            if not isinstance(child_node, Assign):
                continue
            # We are only interested in assignments to a call
            if not isinstance(child_node.value, Call):
                continue
            # Encountered values: "ForeignKey", "OneToOneField" or "models.ForeignKey", "models.OneToOneField"
            # because they can be ast Name or Attribute nodes
            child_node_name = child_node.value.func.as_string().split(".")[-1]
            # We are only interested in ForeignKey and OneToOneField fields
            if child_node_name not in ("ForeignKey", "OneToOneField"):
                continue

            # Check if this field references JobResult
            # The model reference can be a positional argument or the 'to' keyword argument
            jobresult_reference = False

            # Check positional arguments (first arg is the model)
            if child_node.value.args:
                first_arg = child_node.value.args[0]
                if _is_jobresult_reference(first_arg):
                    jobresult_reference = True

            # Check keyword arguments (to= is the model)
            if not jobresult_reference:
                for keyword in child_node.value.keywords:
                    if keyword.arg == "to":
                        if _is_jobresult_reference(keyword.value):
                            jobresult_reference = True
                        break

            if not jobresult_reference:
                continue

            # Check if on_delete is PROTECT
            for keyword in child_node.value.keywords:
                if keyword.arg == "on_delete":
                    if _is_protect(keyword.value):
                        self.add_message("nb-jobresult-on-delete-protect", node=child_node)
                    break
