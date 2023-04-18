"""Utilities for managing data."""
from importlib_resources import files
from yaml import safe_load


def load_v2_code_location_changes():
    """Black magic data transform, needs schema badly."""
    with open(files("pylint_nautobot") / "data" / "v2" / "v2-code-location-changes.yaml", encoding="utf-8") as rules:
        changes = safe_load(rules)
    changes_map = {}
    for change in changes:
        if change["Old Module"] not in changes_map:
            changes_map[change["Old Module"]] = {}
        changes_map[change["Old Module"]][change["Class/Function(s)"]] = change["New Module"]
    return changes_map


MAP_CODE_LOCATION_CHANGES = load_v2_code_location_changes()
