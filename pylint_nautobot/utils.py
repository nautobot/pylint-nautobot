"""Utilities for managing data."""
from importlib import metadata
from pathlib import Path
from typing import Optional
from typing import Union

import toml
from importlib_resources import files
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from yaml import safe_load


def is_nautobot_v2_installed() -> bool:
    """Return True if Nautobot v2.x is installed."""
    return MINIMUM_NAUTOBOT_VERSION.major == 2


def is_version_compatible(specifier_set: Union[str, SpecifierSet]) -> bool:
    """Return True if the Nautobot version is compatible with the given version specifier_set."""
    if not specifier_set:
        return True
    if isinstance(specifier_set, str):
        specifier_set = SpecifierSet(specifier_set)
    return specifier_set.contains(MINIMUM_NAUTOBOT_VERSION)


def load_v2_code_location_changes():
    """Black magic data transform, needs schema badly."""
    with open(files("pylint_nautobot") / "data" / "v2" / "v2-code-location-changes.yaml", encoding="utf-8") as rules:  # type: ignore
        changes = safe_load(rules)
    changes_map = {}
    for change in changes:
        if change["Old Module"] not in changes_map:
            changes_map[change["Old Module"]] = {}
        changes_map[change["Old Module"]][change["Class/Function(s)"]] = change["New Module"]
    return changes_map


def _read_poetry_lock() -> dict:
    for directory in (Path.cwd(), *Path.cwd().parents):
        path = directory / "poetry.lock"
        if path.exists():
            return toml.load(Path(path))

    return {}


def _read_locked_nautobot_version() -> Optional[str]:
    poetry_lock = _read_poetry_lock()
    if not poetry_lock:
        return None

    for package in poetry_lock.get("package", []):
        if package["name"] == "nautobot":
            return package["version"]

    return None


MAP_CODE_LOCATION_CHANGES = load_v2_code_location_changes()
MINIMUM_NAUTOBOT_VERSION = Version(_read_locked_nautobot_version() or metadata.version("nautobot"))
