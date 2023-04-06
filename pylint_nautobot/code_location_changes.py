from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


NAUTOBOT_UTILITIES_MAP = {
    "nautobot.utilities.api": "nautobot.core.api.utils",
    "nautobot.utilities.apps": "nautobot.core.apps",
    "nautobot.utilities.checks": "nautobot.core.checks",
    "nautobot.utilities.choices": "nautobot.core.choices",
    "nautobot.utilities.config": "nautobot.core.utils.config",
    "nautobot.utilities.constants": "nautobot.core.constants",
    "nautobot.utilities.deprecation": "nautobot.core.utils.deprecation",
    "nautobot.utilities.error_handlers": "nautobot.core.views.utils",
    "nautobot.utilities.exceptions": "nautobot.core.exceptions",
    "nautobot.utilities.factory": "nautobot.core.factory",
    "nautobot.utilities.fields": "nautobot.core.models.fields",
    "nautobot.utilities.filters": "nautobot.core.filters",
    "nautobot.utilities.forms": "nautobot.core.forms",
    "nautobot.utilities.git": "nautobot.core.utils.git",
    "nautobot.utilities.logging": "nautobot.core.utils.logging",
    "nautobot.utilities.management": "nautobot.core.management",
    "nautobot.utilities.ordering": "nautobot.core.utils.ordering",
    "nautobot.utilities.paginator": "nautobot.core.views.paginator",
    "nautobot.utilities.permissions": "nautobot.core.utils.permissions",
    "nautobot.utilities.query_functions": "nautobot.core.models.query_functions",
    "nautobot.utilities.querysets": "nautobot.core.models.querysets",
    "nautobot.utilities.tables": "nautobot.core.tables",
    "nautobot.utilities.tasks": "nautobot.core.tasks",
    "nautobot.utilities.templatetags": "nautobot.core.templatetags",
    "nautobot.utilities.testing": "nautobot.core.testing",
    "nautobot.utilities.tree_queries": "nautobot.core.models.tree_queries",
}


class NautobotCodeLocationChangesChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = "nautobot-code-location-changes"
    msgs = {
        "E4251": (
            "Import location has changed (%s -> %s).",
            "nb-code-location-utilities",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#python-code-location-changes",
        ),
    }

    def visit_importfrom(self, node):
        if node.modname in NAUTOBOT_UTILITIES_MAP:
            self.add_message(
                "nb-code-location-utilities",
                node=node,
                args=(node.modname, NAUTOBOT_UTILITIES_MAP[node.modname]),
            )
