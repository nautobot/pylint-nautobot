"""Initialization file for library."""
from pathlib import Path

import tomli
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from pylint.lint import PyLinter

from pylint_nautobot.code_location_changes import NautobotCodeLocationChangesChecker
from pylint_nautobot.deprecated_status_model import NautobotDeprecatedStatusModelChecker
from pylint_nautobot.incorrect_base_class import NautobotIncorrectBaseClassChecker
from pylint_nautobot.model_label import NautobotModelLabelChecker
from pylint_nautobot.replaced_models import NautobotReplacedModelsImportChecker
from pylint_nautobot.string_field_blank_null import NautobotStringFieldBlankNull

try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

CHECKERS = [
    NautobotCodeLocationChangesChecker,
    NautobotDeprecatedStatusModelChecker,
    NautobotIncorrectBaseClassChecker,
    NautobotModelLabelChecker,
    NautobotReplacedModelsImportChecker,
    NautobotStringFieldBlankNull,
]


def _read_target_pyproject_toml() -> dict:
    """Try to discover the target projects 'pyproject.toml' to access its pylint-nautobot configuration."""
    # TODO: It would be great if we could infer this from the Nautobot dependency constraint for the target project.
    for directory in [*Path.cwd().parents, Path.cwd()]:
        pyproject_toml_path = directory / "pyproject.toml"
        if pyproject_toml_path.exists():
            with open(pyproject_toml_path, "rb") as file:
                return tomli.load(file)

    raise RuntimeError("Unable to find pyproject.toml for target project.")


def register(linter: PyLinter):
    """Pylint plugin entrypoint - register all the checks to the linter."""
    pyproject_toml_content = _read_target_pyproject_toml()

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
