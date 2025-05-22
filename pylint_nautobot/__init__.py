"""Initialization file for library."""

from importlib import metadata

from pylint.lint import PyLinter

from .code_location_changes import NautobotCodeLocationChangesChecker
from .deprecated_status_model import NautobotDeprecatedStatusModelChecker
from .incorrect_base_class import NautobotIncorrectBaseClassChecker
from .model_label import NautobotModelLabelChecker
from .q_search_filter import NautobotUseSearchFilterChecker
from .replaced_models import NautobotReplacedModelsImportChecker
from .string_field_blank_null import NautobotStringFieldBlankNull
from .sub_class_name import NautobotSubClassNameChecker
from .use_fields_all import NautobotUseFieldsAllChecker
from .utils import is_version_compatible

__version__ = metadata.version(__name__)

CHECKERS = [
    NautobotCodeLocationChangesChecker,
    NautobotDeprecatedStatusModelChecker,
    NautobotIncorrectBaseClassChecker,
    NautobotModelLabelChecker,
    NautobotReplacedModelsImportChecker,
    NautobotStringFieldBlankNull,
    NautobotSubClassNameChecker,
    NautobotUseFieldsAllChecker,
    NautobotUseSearchFilterChecker,
]


def register(linter: PyLinter):
    """Pylint plugin entrypoint - register all the checks to the linter."""
    for checker in CHECKERS:
        if is_version_compatible(checker.version_specifier):
            linter.register_checker(checker(linter))
