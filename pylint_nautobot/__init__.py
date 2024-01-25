"""Initialization file for library."""
from importlib import metadata
from pathlib import Path

import toml
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from pylint.lint import PyLinter

from pylint_nautobot.code_location_changes import NautobotCodeLocationChangesChecker
from pylint_nautobot.deprecated_status_model import NautobotDeprecatedStatusModelChecker
from pylint_nautobot.incorrect_base_class import NautobotIncorrectBaseClassChecker
from pylint_nautobot.model_label import NautobotModelLabelChecker
from pylint_nautobot.replaced_models import NautobotReplacedModelsImportChecker
from pylint_nautobot.string_field_blank_null import NautobotStringFieldBlankNull

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
            return toml.load(Path(pyproject_toml_path))

    raise RuntimeError("Unable to find pyproject.toml for target project.")


def register(linter: PyLinter):
    """Pylint plugin entrypoint - register all the checks to the linter."""
    pyproject_toml_content = _read_target_pyproject_toml()

    try:
        # TBD: Read minimal supported Nautobot dependency version from poetry.
        # Can be `dev` dependency as well.
        # If there is no Nautobot dependency, use installed Nautobot version.
        # Use single version only, not a list.
        supported_nautobot_versions = [
            Version(version)
            # pylint: disable
            for version in pyproject_toml_content["tool"]["pylint-nautobot"]["supported_nautobot_versions"]
        ]
    except KeyError as error:
        raise ValueError("[tool.pylint-nautobot] configuration missing from pyproject.toml.") from error

    for checker in CHECKERS:
        version_specifier_set = SpecifierSet(checker.version_specifier)
        if not version_specifier_set or any(
            (version in version_specifier_set for version in supported_nautobot_versions)
        ):
            linter.register_checker(checker(linter))
