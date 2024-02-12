"""Utilities for managing data."""

from importlib import metadata
from pathlib import Path
from typing import List
from typing import Optional
from typing import Union

import toml
from astroid import Assign
from astroid import Attribute
from astroid import ClassDef
from astroid import Const
from astroid import Name
from importlib_resources import files
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from yaml import safe_load


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


MINIMUM_NAUTOBOT_VERSION = Version(_read_locked_nautobot_version() or metadata.version("nautobot"))


def is_abstract_class(node: ClassDef) -> bool:
    """Given a node, returns whether it is an abstract base model."""
    for child_node in node.get_children():
        if not (isinstance(child_node, ClassDef) and child_node.name == "Meta"):
            continue

        for meta_child in child_node.get_children():
            if (
                not isinstance(meta_child, Assign)
                or not meta_child.targets[0].name == "abstract"  # type: ignore
                or not isinstance(meta_child.value, Const)
            ):
                continue
            # At this point we know we are dealing with an assignment to a constant for the 'abstract' field on the
            # 'Meta' class. Therefore, we can assume the value of that to be whether the node is an abstract base model
            # or not.
            return meta_child.value.value

    return False


def get_model_name(ancestor: str, node: ClassDef) -> str:
    """Get the model name from the class definition."""
    if ancestor == "from nautobot.apps.views.NautobotUIViewSet":
        raise NotImplementedError("This ancestor is not yet supported.")

    meta = next((n for n in node.body if isinstance(n, ClassDef) and n.name == "Meta"), None)
    if not meta:
        raise NotImplementedError("This class does not have a Meta class.")

    model_attr = next(
        (
            attr
            for attr in meta.body
            if isinstance(attr, Assign)
            and any(
                isinstance(target, (Name, Attribute))
                and getattr(target, "attrname", None) == "model"
                or getattr(target, "name", None) == "model"
                for target in attr.targets
            )
        ),
        None,
    )
    if not model_attr:
        raise NotImplementedError("The Meta class does not define a model attribute.")

    if isinstance(model_attr.value, Name):
        return model_attr.value.name
    if not isinstance(model_attr.value, Attribute):
        raise NotImplementedError("This utility supports only direct assignment or attribute based model names.")

    model_attr_chain = []
    while isinstance(model_attr.value, Attribute):
        model_attr_chain.insert(0, model_attr.value.attrname)
        model_attr.value = model_attr.value.expr

    if isinstance(model_attr.value, Name):
        model_attr_chain.insert(0, model_attr.value.name)

    return model_attr_chain[-1]


def find_ancestor(node: ClassDef, ancestors: List[str]) -> str:
    """Find the class ancestor from the list of ancestors."""
    ancestor_class_types = [ancestor.qname() for ancestor in node.ancestors()]
    for checked_ancestor in ancestors:
        if checked_ancestor in ancestor_class_types:
            return checked_ancestor

    return ""


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


MAP_CODE_LOCATION_CHANGES = load_v2_code_location_changes()
