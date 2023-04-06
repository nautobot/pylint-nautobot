from pylint_nautobot.replaced_models import NautobotReplacedModelsImportChecker
from pylint_nautobot.code_location_changes import NautobotCodeLocationChangesChecker


def register(linter):
    linter.register_checker(NautobotCodeLocationChangesChecker(linter))
    linter.register_checker(NautobotReplacedModelsImportChecker(linter))
