"""Utilities for managing data"""
from yaml import safe_load
from importlib.resources import files


def load_v2_code_location_changes():
    """Black magic data transform, needs schema badly"""
    changes = safe_load(open(files("pylint_nautobot") / "data" / "v2" / "v2-code-location-changes.yaml"))
    changes_map = {}
    for change in changes:
        if change["Old Module"] not in changes_map:
            changes_map[change["Old Module"]] = {}
        changes_map[change["Old Module"]][change["Class/Function(s)"]] = change["New Module"]
    return changes_map


MAP_CODE_LOCATION_CHANGES = load_v2_code_location_changes()
