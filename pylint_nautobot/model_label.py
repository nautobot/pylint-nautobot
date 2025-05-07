"""Check model label construction in f-strings."""

from astroid import Attribute, Const, FormattedValue, JoinedStr, Name, NodeNG
from pylint.checkers import BaseChecker
from pylint.interfaces import HIGH


def _get_model_name_for_meta_attr(node: NodeNG, expected_attrname: str) -> str:
    """Return `<model name>` if `node` contains `<model name>._meta.<expected_attrname>`."""
    if not isinstance(node, FormattedValue):
        return ""
    value = node.value
    if not isinstance(value, Attribute) or value.attrname != expected_attrname:
        return ""
    expr = value.expr
    if not isinstance(expr, Attribute) or expr.attrname != "_meta":
        return ""
    expr = expr.expr
    return (expr.name or "") if isinstance(expr, Name) else ""


def _expect_app_label(state, node: NodeNG) -> bool:
    name = _get_model_name_for_meta_attr(node, "app_label")
    if name:
        state["model_name"] = name
        return True

    return False


def _expect_dot(_, node: NodeNG) -> bool:
    return isinstance(node, Const) and node.value == "."


def _expect_model(state, node: NodeNG) -> bool:
    return _get_model_name_for_meta_attr(node, "model") == state["model_name"]


_EXPECTATIONS = (
    _expect_app_label,
    _expect_dot,
    _expect_model,
)


class NautobotModelLabelChecker(BaseChecker):
    """Model label construction checker."""

    version_specifier = ">=1,<4"

    name = "nautobot-model-label"
    msgs = {
        "C4701": (
            "Model's 'app_label.model_name' should be retrieved with 'model._meta.label_lower'",
            "nb-used-model-label-construction",
            "Replace f-string '{model._meta.app_label}.{model._meta.model}' with '{model._meta.label_lower}'.",
        ),
    }

    def visit_joinedstr(self, node: JoinedStr):
        """Check for f-strings that construct a model's label.

        Matches the following pattern inside the f-string:
            {model._meta.app_label}.{model._meta.model}

        'model' can be any variable name, its value is cached inside 'state["model_name"]' and used to check the next
        node.

        Function iterates node.values (list of AST nodes the f-string is composed of) and checks if the nodes match
        the expectations. Expectations are functions that return True if the node matches, False otherwise.
        When the node matches the expectation, the next function is called for the next node.
        If all functions return True, the message is emitted.
        """
        expectation_index = 0
        state = {"model_name": ""}
        for value in node.values:
            if _EXPECTATIONS[expectation_index](state, value):
                expectation_index += 1
                if expectation_index >= len(_EXPECTATIONS):
                    self.add_message("nb-used-model-label-construction", node=node, confidence=HIGH)
                    break
            else:
                expectation_index = 0
