"""Initialization file for library."""
from pathlib import Path

from packaging.specifiers import SpecifierSet
from packaging.version import Version
from pylint.lint import PyLinter
import tomli


try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from pylint_nautobot.code_location_changes import NautobotCodeLocationChangesChecker
from pylint_nautobot.replaced_models import NautobotReplacedModelsImportChecker
from pylint_nautobot.status_field_instead_of_status_model import NautobotDeprecatedStatusModelChecker
from pylint_nautobot.string_field_null_blank import NautobotStringFieldBlankNull

CHECKERS = [
    NautobotCodeLocationChangesChecker,
    NautobotDeprecatedStatusModelChecker,
    NautobotReplacedModelsImportChecker,
    NautobotStringFieldBlankNull,
]


def register(linter: PyLinter):
    """Pylint plugin entrypoint - register all the checks to the linter."""
    # Try to discover the target projects 'pyproject.toml' to access its pylint-nautobot configuration.
    # TODO: It would be great if we could infer this from the Nautobot dependency constraint for the target project.
    pyproject_toml_content = None
    for directory in [*Path.cwd().parents, Path.cwd()]:
        pyproject_toml_path = directory / "pyproject.toml"
        if pyproject_toml_path.exists():
            with open(pyproject_toml_path, "rb") as file:
                pyproject_toml_content = tomli.load(file)
                break
    try:
        supported_nautobot_versions = [
            Version(version)
            for version in pyproject_toml_content["tool"]["pylint-nautobot"]["supported_nautobot_versions"]
        ]
    except KeyError as error:
        raise Exception("[tool.pylint-nautobot] configuration missing from pyproject.toml.") from error

    for checker in CHECKERS:
        version_specifier_set = SpecifierSet(checker.version_specifier)
        if not version_specifier_set or any(
            (version in version_specifier_set for version in supported_nautobot_versions)
        ):
            linter.register_checker(checker(linter))
