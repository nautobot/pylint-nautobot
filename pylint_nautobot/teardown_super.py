"""Check for tearDown methods that don't call super().tearDown()."""

from astroid.nodes import Attribute, Call, ClassDef, FunctionDef, Name
from pylint.checkers import BaseChecker


def _has_super_teardown_call(node: FunctionDef) -> bool:
    """Check if a function body contains a call to super().tearDown()."""
    for child in node.nodes_of_class(Call):
        func = child.func
        if (
            isinstance(func, Attribute)
            and func.attrname == "tearDown"
            and isinstance(func.expr, Call)
            and isinstance(func.expr.func, Name)
            and func.expr.func.name == "super"
        ):
            return True
    return False


class NautobotTearDownSuperChecker(BaseChecker):
    """Ensure tearDown methods call super().tearDown()."""

    version_specifier = ">=2,<4"

    name = "nautobot-teardown-super"
    msgs = {
        "E4231": (
            "tearDown method should call super().tearDown().",
            "nb-teardown-super",
            "All tearDown methods should call super().tearDown() to ensure proper test cleanup.",
        ),
    }

    def visit_functiondef(self, node: FunctionDef):
        """Visit function definitions looking for tearDown methods."""
        if node.name != "tearDown":
            return

        if not isinstance(node.parent, ClassDef):
            return

        if not _has_super_teardown_call(node):
            self.add_message("nb-teardown-super", node=node)
