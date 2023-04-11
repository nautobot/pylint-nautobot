"""Initialization file for library."""

try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from pylint_nautobot.replaced_models import NautobotReplacedModelsImportChecker
from pylint_nautobot.code_location_changes import NautobotCodeLocationChangesChecker


def register(linter):
    """Pylint plugin entrypoint - register all the checks to the linter."""
    linter.register_checker(NautobotCodeLocationChangesChecker(linter))
    linter.register_checker(NautobotReplacedModelsImportChecker(linter))
