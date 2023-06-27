"""Check model label construction in f-strings."""
from astroid import Attribute
from astroid import Const
from astroid import FormattedValue
from astroid import JoinedStr
from astroid import Name
from astroid import NodeNG
from pylint.checkers import BaseChecker
from pylint.interfaces import HIGH
from pylint.interfaces import IAstroidChecker


def _get_model_name(node: NodeNG, attrname: str) -> str:
    if not isinstance(node, FormattedValue):
        return ""
    value = node.value
    if not isinstance(value, Attribute) or value.attrname != attrname:
        return ""
    expr = value.expr
    if not isinstance(expr, Attribute) or expr.attrname != "_meta":
        return ""
    expr = expr.expr
    return (expr.name or "") if isinstance(expr, Name) else ""


def _expect_app_label(state, node: NodeNG) -> bool:
    name = _get_model_name(node, "app_label")
    if name:
        state["model_name"] = name
        return True

    return False


def _expect_dot(_, node: NodeNG) -> bool:
    return isinstance(node, Const) and node.value == "."


def _expect_model(state, node: NodeNG) -> bool:
    return _get_model_name(node, "model") == state["model_name"]


_EXPECTATIONS = (
    _expect_app_label,
    _expect_dot,
    _expect_model,
)


class NautobotModelLabelChecker(BaseChecker):
    """Model label construction checker."""

    __implements__ = IAstroidChecker

    version_specifier = ">=2,<3"

    name = "model-label-checker"
    msgs = {
        "E7401": (
            "Model's app_label.model_name should be retrieved with `model._meta.label_lower`",
            "used-model-label-construction",
            "Replace f-string `{model._meta.app_label}.{model._meta.model}` with `{model._meta.label_lower}`",
        ),
    }

    def visit_joinedstr(self, node: JoinedStr):
        """Check for f-strings that construct a model's label."""
        state_index = 0
        state = {"model_name": ""}
        for value in node.values:
            if _EXPECTATIONS[state_index](state, value):
                state_index += 1
                if state_index >= len(_EXPECTATIONS):
                    self.add_message("used-model-label-construction", node=node, confidence=HIGH)
                    break
            else:
                state_index = 0
