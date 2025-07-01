"""Utilities for managing data."""

from importlib import metadata
from pathlib import Path
from typing import Callable, Iterable, Optional, TypeVar, Union

import toml
from astroid import Assign, Attribute, Call, ClassDef, Const, Name, NodeNG
from importlib_resources import files
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from yaml import safe_load

T = TypeVar("T")


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


def trim_first_pascal_word(pascal_case_string: str) -> str:
    """Remove the first word from a pascal case string.

    Examples:
    >>> trim_first_pascal_word("NautobotFilterSet")
    'FilterSet'
    >>> trim_first_pascal_word("BaseTable")
    'Table'
    >>> trim_first_pascal_word("FQDNModel")
    'Model'
    """
    start_index = 0

    for i in range(1, len(pascal_case_string)):
        if pascal_case_string[i].isupper():
            start_index = i
            break

    return pascal_case_string[start_index:]


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


def find_attr(node: ClassDef, attr_name: str) -> Optional[Assign]:
    """Get the attribute from the class definition."""
    for attr in node.body:
        if isinstance(attr, Assign):
            for target in attr.targets:
                if (
                    isinstance(target, (Name, Attribute))
                    and getattr(target, "attrname", None) == attr_name
                    or getattr(target, "name", None) == attr_name
                ):
                    return attr
    return None


def find_meta(node: ClassDef) -> Optional[ClassDef]:
    """Find the Meta class from the class definition."""
    for child in node.body:
        if isinstance(child, ClassDef) and child.name == "Meta":
            return child
    return None


def find_model_name(node: ClassDef) -> str:
    """Get the model name from the class definition."""
    queryset = find_attr(node, "queryset")
    if queryset:
        return get_model_name_from_queryset(queryset.value)

    if meta := find_meta(node):
        model_attr = find_attr(meta, "model")
        if not model_attr:
            return ""
    elif not (model_attr := find_attr(node, "model")):
        return ""

    return get_model_name_from_attr(model_attr)


def get_model_name_from_queryset(node: NodeNG) -> str:
    """Get the model name from the queryset assignment value."""
    while node:
        if isinstance(node, Call):
            node = node.func
        elif isinstance(node, Attribute):
            if node.attrname == "objects":
                if isinstance(node.expr, Name):
                    # Covers `queryset = AddressObject.objects.all()`
                    return node.expr.name
                if isinstance(node.expr, Attribute):
                    # Covers `queryset = models.AddressObject.objects.all()`
                    return node.expr.attrname
            node = node.expr
        else:
            break

    raise NotImplementedError("Model was not found")


def get_model_name_from_attr(model_attr: Assign) -> str:
    """Get the model name from the model attribute."""
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


def find_ancestor(
    node: ClassDef, ancestors: Iterable[T], get_value: Optional[Callable[[T], str]] = None
) -> Optional[T]:
    """Find the class ancestor from the list of ancestors."""
    ancestor_class_types = [ancestor.qname() for ancestor in node.ancestors()]
    for checked_ancestor in ancestors:
        if get_value and get_value(checked_ancestor) in ancestor_class_types:
            return checked_ancestor
        if not get_value and checked_ancestor in ancestor_class_types:
            return checked_ancestor

    return None


def is_version_compatible(specifier_set: Union[str, SpecifierSet]) -> bool:
    """Return True if the Nautobot version is compatible with the given version specifier_set."""
    if not specifier_set:
        return True
    if isinstance(specifier_set, str):
        specifier_set = SpecifierSet(specifier_set, prereleases=True)
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
