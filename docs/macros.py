"""mkdocs-macros-plugin data loading"""

from pylint_nautobot import get_rules

def define_env(env):
    env.variables["pylint_nautobot_rules"] = sorted(get_rules())
