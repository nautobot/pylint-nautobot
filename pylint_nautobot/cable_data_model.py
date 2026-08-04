"""Check for code impacted by the Nautobot 3.2 Cable data model changes.

In Nautobot 3.2 the `cable` `ForeignKey` on every `CableTermination` subclass (`Interface`, `FrontPort`,
`CircuitTermination`, ...) was replaced by the `CableToCableTermination` join model, reached via the
`cable_termination` reverse one-to-one relation, and `Cable.termination_a`/`Cable.termination_b` were
replaced by the `Cable.terminations` relation. Backwards-compatibility shims cover the most common access
patterns; the checks in this module flag the patterns that either break outright or are only supported
through a deprecated shim.

Reference:
https://docs.nautobot.com/projects/core/en/stable/release-notes/version-3.2/#migrate-cable-termination-queries
"""

from astroid.nodes import Assign, AssignAttr, Attribute, Call, Const, List, Name, NodeNG, Set, Tuple
from pylint.checkers import BaseChecker

# Django's async ORM variants delegate to their sync counterparts, so they reach the same shims and are
# classified identically. Only the methods Django actually provides an `a`-prefixed form for are listed.

# Queryset methods whose keyword arguments are field lookups that the 3.2 shims rewrite.
TRANSLATED_LOOKUP_METHODS = frozenset({"aget", "exclude", "filter", "get"})

# `Cable.objects` also routes the lookup half of these through `filter()`/`get()`.
CABLE_TRANSLATED_LOOKUP_METHODS = TRANSLATED_LOOKUP_METHODS | {
    "aget_or_create",
    "aupdate_or_create",
    "get_or_create",
    "update_or_create",
}

# Methods that assign to the named fields rather than (only) querying them.
CREATE_METHODS = frozenset(
    {"acreate", "aget_or_create", "aupdate_or_create", "create", "get_or_create", "update_or_create"}
)

# `Cable.objects.create(termination_a=..., termination_b=...)` is the documented replacement pattern, so unlike
# the `*_or_create` methods it has no lookup half to deprecate.
PURE_CREATE_METHODS = frozenset({"acreate", "create"})

# Keywords here name fields directly, with no shim: `Q()` bypasses the queryset, and `update()` resolves against
# real fields (so even `update(cable=None)` fails, unlike `create(cable=None)`). `annotate()`/`aggregate()`/
# `alias()` are excluded on purpose - their keywords are caller-invented output aliases, not field paths.
DIRECT_FIELD_KWARG_CALLABLES = frozenset({"Q", "aupdate", "update"})

# Callables naming a single field rather than a lookup path. `get_field()` resolves the reverse relation happily,
# so it can be pointed at `cable_termination`.
RELATION_NAME_CALLABLES = frozenset({"get_field"})

# Callables naming *concrete* fields to read or write. The cable link is no longer a field on the termination at
# all, and `cable_termination` is a reverse relation rather than a concrete field, so these reject it too - the
# join record has to be handled directly instead.
JOIN_MODEL_CALLABLES = frozenset(
    {
        "abulk_update",
        "arefresh_from_db",
        "asave",
        "aupdate",
        "bulk_update",
        "refresh_from_db",
        "save",
        "update",
    }
)

# Callables taking a collection of field names, as `{callable: (keyword name, positional index or None)}`.
FIELD_NAME_LIST_ARGUMENTS = {
    "abulk_update": ("fields", 1),
    "arefresh_from_db": ("fields", 1),
    "asave": ("update_fields", None),
    "bulk_update": ("fields", 1),
    "refresh_from_db": ("fields", 1),
    "save": ("update_fields", None),
}

# All callables whose keyword arguments should be inspected as field lookups.
KEYWORD_LOOKUP_CALLABLES = (
    TRANSLATED_LOOKUP_METHODS | CABLE_TRANSLATED_LOOKUP_METHODS | CREATE_METHODS | DIRECT_FIELD_KWARG_CALLABLES
)

# Methods whose positional string arguments are field names or lookup paths. Mostly queryset methods, plus
# `Options.get_field()`, which raises FieldDoesNotExist for anything that is now only a property.
FIELD_NAME_ARGUMENT_METHODS = frozenset(
    {
        "aearliest",
        "alatest",
        "dates",
        "datetimes",
        "defer",
        "distinct",
        "earliest",
        "get_field",
        "latest",
        "only",
        "order_by",
        "prefetch_related",
        "select_related",
        "values",
        "values_list",
    }
)

# Query expressions whose positional string arguments are field names or lookup paths.
FIELD_NAME_EXPRESSIONS = frozenset(
    {"Avg", "Count", "F", "FilteredRelation", "Max", "Min", "OuterRef", "Prefetch", "Sum"}
)

# Roots of a lookup path that referenced the removed `CableTermination.cable` foreign key.
CABLE_ROOTS = frozenset({"cable", "cable_id"})

# Models and relation accessors on which `cable`/`cable_id` is a real field in Nautobot 3.2, rather than the
# removed CableTermination foreign key. `CableToCableTermination` *is* the new join model, and the
# `cable_termination` / `terminations` accessors reach it, so queries against those are already correct.
CABLE_JOIN_RECEIVERS = frozenset({"CableToCableTermination", "cable_termination", "cable_terminations", "terminations"})

# Roots of a lookup path that referenced the removed `Cable.termination_[ab]` generic foreign keys.
LEGACY_TERMINATION_ROOTS = frozenset(
    {
        "termination_a",
        "termination_a_id",
        "termination_a_type",
        "termination_a_type_id",
        "termination_b",
        "termination_b_id",
        "termination_b_type",
        "termination_b_type_id",
    }
)

# The subset of the above that `CableQuerySet` rewrites, and only as exact (non-transformed) lookups.
TRANSLATED_TERMINATION_LOOKUPS = LEGACY_TERMINATION_ROOTS - {"termination_a", "termination_b"}

# Private cache fields removed from `CableTermination` without a compatibility shim.
REMOVED_CABLE_PEER_FIELDS = frozenset({"_cable_peer", "_cable_peer_id", "_cable_peer_type"})

# The private `PathEndpoint._path` foreign key, replaced by the `cable_paths` generic relation.
PATH_FIELD = "_path"

_REFERENCE = (
    "Reference: https://docs.nautobot.com/projects/core/en/stable/release-notes/version-3.2/"
    "#migrate-cable-termination-queries"
)


def split_lookup_path(path: str) -> tuple[str, str, str]:
    """Split a lookup path into its `order_by` direction prefix, root field name, and remaining lookups.

    Examples:
    >>> split_lookup_path("cable")
    ('', 'cable', '')
    >>> split_lookup_path("-cable__status__name")
    ('-', 'cable', '__status__name')
    >>> split_lookup_path("cable_id__in")
    ('', 'cable_id', '__in')
    """
    prefix = "-" if path.startswith("-") else ""
    root, separator, rest = path[len(prefix) :].partition("__")
    return prefix, root, f"{separator}{rest}" if separator else ""


def translate_path_cable_to_cable_termination__cable(path: str) -> str:
    """Rewrite a lookup path rooted at the removed `cable` field onto the `cable_termination` relation.

    Examples:
    >>> translate_path_cable_to_cable_termination__cable("cable")
    'cable_termination__cable'
    >>> translate_path_cable_to_cable_termination__cable("-cable__status")
    '-cable_termination__cable__status'
    """
    prefix, root, rest = split_lookup_path(path)
    return f"{prefix}cable_termination__{root}{rest}"


def translate_path__path_to_cable_paths(path: str) -> str:
    """Rewrite a lookup path rooted at the removed `_path` field onto the `cable_paths` relation.

    Examples:
    >>> translate_path__path_to_cable_paths("_path__destination_id")
    'cable_paths__destination_id'
    """
    prefix, _, rest = split_lookup_path(path)
    return f"{prefix}cable_paths{rest}"


def cable_replacement(name: str, path: str) -> str:
    """Suggest the replacement for a `cable`-rooted reference made by the callable `name`.

    Examples:
    >>> cable_replacement("order_by", "-cable__status")
    '-cable_termination__cable__status'
    >>> cable_replacement("get_field", "cable")
    'cable_termination'
    >>> cable_replacement("save", "cable")
    'CableToCableTermination'
    """
    if name in RELATION_NAME_CALLABLES:
        return "cable_termination"
    if name in JOIN_MODEL_CALLABLES:
        return "CableToCableTermination"
    return translate_path_cable_to_cable_termination__cable(path)


def called_name(node: Call) -> str:
    """Return the name of the called function or method.

    For example, returns `"filter"` for `Interface.objects.filter(...)` and `"Q"` for both `Q(...)` and
    `models.Q(...)`.
    """
    func = node.func
    if isinstance(func, Attribute):
        return func.attrname
    if isinstance(func, Name):
        return func.name
    return ""


def is_none(node: NodeNG) -> bool:
    """Return whether the given node is the literal `None`."""
    return isinstance(node, Const) and node.value is None


def targets_cable_join_model(node: Call) -> bool:
    """Return whether a call is made against the `CableToCableTermination` join model or a relation reaching it.

    `CableToCableTermination` has real `cable` and `cable_id` fields, so `cable`-rooted lookups against it (e.g.
    `CableToCableTermination.objects.filter(cable=cable)` or `cable.terminations.values("cable_id")`) are the
    already-migrated form (and therefore shouldn't be flagged) rather than a use of the removed CableTermination FK.
    """
    names = set()
    expression = node.func
    while True:
        if isinstance(expression, Attribute):
            names.add(expression.attrname)
            expression = expression.expr
        elif isinstance(expression, Call):
            # Step over an intermediate call in a chain, e.g. `...objects.filter(x).values("cable_id")`.
            expression = expression.func
        else:
            if isinstance(expression, Name):
                names.add(expression.name)
            break
    return bool(names & CABLE_JOIN_RECEIVERS)


class NautobotCableDataModelChecker(BaseChecker):
    """Flag queries and attribute usage broken or deprecated by the Nautobot 3.2 Cable data model changes."""

    # The replacement APIs (`cable_termination`, `CableToCableTermination`, `Cable.terminations`, `cable_paths`)
    # only exist as of Nautobot 3.2, so these checks would misdirect apps targeting an earlier version. There is
    # no upper bound: the removed fields stay removed, and the deprecated shims flagged here are candidates for
    # removal in a future major version, which would turn those warnings into hard failures rather than retire them.
    version_specifier = ">=3.2"

    name = "nautobot-cable-data-model"
    msgs = {
        "E4231": (
            "Reference to `%s` is not translated by the Nautobot 3.2 compatibility shim; use `%s` instead.",
            "nb-removed-cable-field",
            "The `cable` foreign key was removed from CableTermination subclasses in Nautobot 3.2. Only "
            "`filter()`/`exclude()`/`get()` keyword lookups and `select_related()` are rewritten by the "
            "compatibility shim; every other reference must be rewritten against the `cable_termination` "
            f"relation. {_REFERENCE}",
        ),
        "W4232": (
            "Querying by `%s` is deprecated in Nautobot 3.2; use `%s` instead.",
            "nb-deprecated-cable-lookup",
            "The `cable` foreign key was removed from CableTermination subclasses in Nautobot 3.2. This lookup "
            "still works, but is rewritten onto the `cable_termination` relation by a compatibility shim that "
            "raises a DeprecationWarning. The replacement does not exist before Nautobot 3.2, so an App that "
            "still supports earlier versions has no alternative spelling available and should disable this "
            f"check explicitly until support for Nautobot < 3.2 is dropped. {_REFERENCE}",
        ),
        "E4233": (
            "Assigning a Cable to `%s` is not supported in Nautobot 3.2.",
            "nb-readonly-cable-attribute",
            "In Nautobot 3.2 a termination's `cable` attribute is a read-only property, and assigning anything "
            "other than `None` to it raises NotImplementedError. Use "
            "`Cable.objects.create(termination_a=..., termination_b=...)`, `Cable.add_termination()`, or create a "
            f"`CableToCableTermination` record directly. {_REFERENCE}",
        ),
        "E4234": (
            "Reference to `%s` is not translated by the Nautobot 3.2 compatibility shim; "
            "use the `terminations` relation instead.",
            "nb-removed-termination-a-b-field",
            "The `termination_a`/`termination_b` generic foreign keys are no longer database fields on Cable in "
            "Nautobot 3.2. Only exact `termination_[ab]_[type|type_id|id]` keyword lookups are rewritten by the "
            "compatibility shim; every other reference must be rewritten against the `terminations` "
            f"(CableToCableTermination) relation. {_REFERENCE}",
        ),
        "W4235": (
            "Querying Cable by `%s` is deprecated in Nautobot 3.2; use the `terminations` relation instead.",
            "nb-deprecated-termination-a-b-lookup",
            "The `termination_a`/`termination_b` generic foreign keys are no longer database fields on Cable in "
            "Nautobot 3.2. This lookup still works, but is rewritten onto the `terminations` relation by a "
            "compatibility shim that raises a DeprecationWarning. Note that such lookups only ever match the "
            "first connector on each side of a Cable, so they cannot describe a breakout cable. The replacement "
            "does not exist before Nautobot 3.2, so an App that still supports earlier versions has no "
            "alternative spelling available and should disable this check explicitly until support for "
            f"Nautobot < 3.2 is dropped. {_REFERENCE}",
        ),
        "W4236": (
            "Excluding on both Cable termination ends at once is not equivalent in Nautobot 3.2.",
            "nb-termination-a-b-exclude-both-ends",
            "The Nautobot 3.2 compatibility shim applies each end of the exclusion independently "
            "(`exclude(A) AND exclude(B)`), which is not the same as negating the combined condition, because "
            "the A-side and B-side match different CableToCableTermination records. Use separate `exclude()` "
            f"calls or an explicit `terminations__...` Q object. {_REFERENCE}",
        ),
        "E4237": (
            "The `_path` field was replaced by the `cable_paths` relation in Nautobot 3.2; use `%s` instead.",
            "nb-removed-cable-path-field",
            "The private `_path` foreign key on PathEndpoint was replaced by a `cable_paths` GenericRelation in "
            "Nautobot 3.2. Because this is now a multi-row reverse relation (one CablePath per breakout lane), "
            f"`distinct()` is typically required on `filter()`/`count()`/`exclude()`. {_REFERENCE}",
        ),
        "E4238": (
            "The `%s` field was removed in Nautobot 3.2.",
            "nb-removed-cable-peer-field",
            "The private `_cable_peer`, `_cable_peer_type`, and `_cable_peer_id` cache fields were removed from "
            "CableTermination in Nautobot 3.2 without a compatibility shim. Use `get_cable_peer()` (or "
            f"`get_cable_peers()` for breakout cables) instead. {_REFERENCE}",
        ),
    }

    def visit_assign(self, node: Assign):
        """Check for assignment to a termination's now read-only `cable` property."""
        if is_none(node.value):
            # `termination.cable = None` is still supported and disconnects the termination on save().
            return

        for target in node.targets:
            if not isinstance(target, AssignAttr) or target.attrname != "cable":
                continue
            if isinstance(target.expr, Name) and target.expr.name in ("cls", "self"):
                # Too likely to be an unrelated attribute of the enclosing class to be worth flagging.
                continue
            self.add_message("nb-readonly-cable-attribute", node=node, args=(target.as_string(),))

    def visit_attribute(self, node: Attribute):
        """Check for access to the removed private cable peer cache fields."""
        self._check_cable_peer_attribute(node)

    def visit_assignattr(self, node: AssignAttr):
        """Check for assignment to the removed private cable peer cache fields."""
        self._check_cable_peer_attribute(node)

    def _check_cable_peer_attribute(self, node: NodeNG):
        """Report access to or assignment of a removed private cable peer cache field."""
        if node.attrname in REMOVED_CABLE_PEER_FIELDS:
            self.add_message("nb-removed-cable-peer-field", node=node, args=(node.attrname,))

    def visit_call(self, node: Call):
        """Check the keyword lookups and field-name arguments of a query call."""
        name = called_name(node)
        if not name:
            return

        joins_cable_terminations = targets_cable_join_model(node)
        self._check_keyword_lookups(node, name, joins_cable_terminations)
        self._check_field_name_arguments(node, name, joins_cable_terminations)
        self._check_field_name_list_arguments(node, name, joins_cable_terminations)

    def _check_keyword_lookups(self, node: Call, name: str, joins_cable_terminations: bool):  # noqa:PLR0912 pylint: disable=too-many-branches
        """Check `field__lookup=value` style keyword arguments of a query call."""
        if name not in KEYWORD_LOOKUP_CALLABLES:
            return

        # Legacy `Cable.termination_[ab]*` lookups are reported once per cable end rather than once per keyword,
        # as a single call commonly names both the `*_type` and the `*_id` of the same end.
        translated_by_end = {"a": [], "b": []}

        for keyword in node.keywords:
            path = keyword.arg
            if not path:
                continue
            _, root, rest = split_lookup_path(path)
            if root in CABLE_ROOTS:
                if not joins_cable_terminations:
                    self._check_cable_lookup(node, name, path, rest, keyword.value)
            elif root in LEGACY_TERMINATION_ROOTS:
                if not rest and root in TRANSLATED_TERMINATION_LOOKUPS and name in CABLE_TRANSLATED_LOOKUP_METHODS:
                    translated_by_end[root.split("_")[1]].append(path)
                elif name not in PURE_CREATE_METHODS:
                    self.add_message("nb-removed-termination-a-b-field", node=node, args=(path,))
            elif root == PATH_FIELD:
                self.add_message(
                    "nb-removed-cable-path-field", node=node, args=(translate_path__path_to_cable_paths(path),)
                )
            elif root in REMOVED_CABLE_PEER_FIELDS:
                self.add_message("nb-removed-cable-peer-field", node=node, args=(root,))

        if name == "exclude" and all(translated_by_end.values()):
            # Each end is excluded independently, which does not negate the combined condition.
            self.add_message("nb-termination-a-b-exclude-both-ends", node=node)
            return

        for paths in translated_by_end.values():
            if paths:
                self.add_message("nb-deprecated-termination-a-b-lookup", node=node, args=(", ".join(paths),))

    def _check_cable_lookup(self, node: Call, name: str, path: str, rest: str, value: NodeNG):
        """Check a single keyword lookup rooted at the removed `CableTermination.cable` field."""
        if name in CREATE_METHODS:
            # `Interface.objects.create(cable=...)` reaches the `cable` property setter and raises.
            if not is_none(value):
                self.add_message("nb-readonly-cable-attribute", node=node, args=(path,))

        elif name in TRANSLATED_LOOKUP_METHODS:
            if not rest and is_none(value):
                # Absence of a cable is now the absence of a join record rather than a null foreign key.
                replacement = "cable_termination__isnull=True"
            elif rest == "__isnull":
                replacement = "cable_termination__isnull"
            else:
                replacement = translate_path_cable_to_cable_termination__cable(path)
            self.add_message("nb-deprecated-cable-lookup", node=node, args=(path, replacement))

        else:
            self.add_message("nb-removed-cable-field", node=node, args=(path, cable_replacement(name, path)))

    def _check_field_name_arguments(self, node: Call, name: str, joins_cable_terminations: bool):
        """Check positional string arguments that Django interprets as field names or lookup paths."""
        if name not in FIELD_NAME_ARGUMENT_METHODS and name not in FIELD_NAME_EXPRESSIONS:
            return

        for argument in node.args:
            self._check_field_name(argument, name, joins_cable_terminations)

    def _check_field_name_list_arguments(self, node: Call, name: str, joins_cable_terminations: bool):
        """Check arguments holding a collection of field names, e.g. `save(update_fields=["cable"])`."""
        spec = FIELD_NAME_LIST_ARGUMENTS.get(name)
        if spec is None:
            return

        keyword_name, position = spec
        collection = next((keyword.value for keyword in node.keywords if keyword.arg == keyword_name), None)
        if collection is None and position is not None and len(node.args) > position:
            collection = node.args[position]
        if not isinstance(collection, (List, Set, Tuple)):
            return

        for element in collection.elts:
            self._check_field_name(element, name, joins_cable_terminations)

    def _check_field_name(self, argument: NodeNG, name: str, joins_cable_terminations: bool):
        """Report a single string node that Django interprets as a field name or lookup path."""
        if not isinstance(argument, Const) or not isinstance(argument.value, str):
            return

        path = argument.value
        _, root, _ = split_lookup_path(path)
        if root in CABLE_ROOTS:
            if joins_cable_terminations:
                return
            if name == "select_related" and root == "cable":
                self.add_message(
                    "nb-deprecated-cable-lookup",
                    node=argument,
                    args=(path, translate_path_cable_to_cable_termination__cable(path)),
                )
            else:
                self.add_message("nb-removed-cable-field", node=argument, args=(path, cable_replacement(name, path)))
        elif root in LEGACY_TERMINATION_ROOTS:
            self.add_message("nb-removed-termination-a-b-field", node=argument, args=(path,))
        elif root == PATH_FIELD:
            self.add_message(
                "nb-removed-cable-path-field", node=argument, args=(translate_path__path_to_cable_paths(path),)
            )
        elif root in REMOVED_CABLE_PEER_FIELDS:
            self.add_message("nb-removed-cable-peer-field", node=argument, args=(root,))
