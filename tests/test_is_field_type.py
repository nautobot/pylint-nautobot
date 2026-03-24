"""Tests for the is_field_type utility function."""

import astroid

from pylint_nautobot.utils import is_field_type

FOREIGN_KEY_QNAMES = (
    "django.db.models.fields.related.ForeignKey",
    "django.db.models.fields.related.OneToOneField",
)

TEXT_FIELD_QNAMES = (
    "django.db.models.fields.CharField",
    "django.db.models.fields.TextField",
)


def _get_func_node(code, class_name="MyModel", assign_index=0):
    """Parse code and return the func node of a Call assignment in the given class."""
    module = astroid.parse(code)
    for node in module.body:
        if isinstance(node, astroid.nodes.ClassDef) and node.name == class_name:
            assigns = [child for child in node.body if isinstance(child, astroid.nodes.Assign)]
            return assigns[assign_index].value.func
    raise ValueError(f"Class {class_name} not found")


class TestIsFieldTypeStringFallback:
    """Tests for string-based fallback matching (when safe_infer returns None)."""

    def test_direct_name_foreignkey(self):
        code = """
class MyModel:
    field = ForeignKey("SomeModel", on_delete=PROTECT)
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, FOREIGN_KEY_QNAMES) is True

    def test_direct_name_onetoonefield(self):
        code = """
class MyModel:
    field = OneToOneField("SomeModel", on_delete=PROTECT)
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, FOREIGN_KEY_QNAMES) is True

    def test_dotted_models_foreignkey(self):
        code = """
class MyModel:
    field = models.ForeignKey("SomeModel", on_delete=PROTECT)
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, FOREIGN_KEY_QNAMES) is True

    def test_dotted_models_onetoonefield(self):
        code = """
class MyModel:
    field = models.OneToOneField("SomeModel", on_delete=PROTECT)
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, FOREIGN_KEY_QNAMES) is True

    def test_non_matching_field(self):
        code = """
class MyModel:
    field = CharField(max_length=100)
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, FOREIGN_KEY_QNAMES) is False

    def test_non_matching_dotted_field(self):
        code = """
class MyModel:
    field = models.CharField(max_length=100)
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, FOREIGN_KEY_QNAMES) is False

    def test_charfield_match(self):
        code = """
class MyModel:
    field = CharField(max_length=100)
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, TEXT_FIELD_QNAMES) is True

    def test_textfield_match(self):
        code = """
class MyModel:
    field = models.TextField()
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, TEXT_FIELD_QNAMES) is True

    def test_completely_unrelated_call(self):
        code = """
class MyModel:
    field = SomeOtherFunction()
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, FOREIGN_KEY_QNAMES) is False

    def test_deeply_dotted_path(self):
        code = """
class MyModel:
    field = django.db.models.ForeignKey("SomeModel", on_delete=PROTECT)
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, FOREIGN_KEY_QNAMES) is True

    def test_empty_field_names(self):
        code = """
class MyModel:
    field = ForeignKey("SomeModel", on_delete=PROTECT)
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, ()) is False


class TestIsFieldTypeInference:
    """Tests for inference-based matching (when safe_infer resolves a ClassDef).

    When classes are defined in the same parsed module, astroid can infer them.
    Parsed modules produce qnames like ".ClassName", so we use those for matching.
    """

    def test_inferred_class_direct_match(self):
        """When safe_infer resolves to a ClassDef whose qname matches directly."""
        code = """
class ForeignKey:
    pass

class MyModel(object):
    field = ForeignKey()
"""
        func_node = _get_func_node(code)
        # Use the qname that astroid.parse produces: ".ForeignKey"
        assert is_field_type(func_node, (".ForeignKey",)) is True

    def test_inferred_class_no_match(self):
        """A class defined locally that doesn't match any field name."""
        code = """
class SomeOtherClass:
    pass

class MyModel(object):
    field = SomeOtherClass()
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, (".ForeignKey",)) is False

    def test_inferred_subclass_via_ancestor(self):
        """When a class inherits from a matching base class, ancestor checking works."""
        code = """
class ForeignKey:
    pass

class CustomForeignKey(ForeignKey):
    pass

class MyModel(object):
    field = CustomForeignKey()
"""
        func_node = _get_func_node(code)
        # CustomForeignKey's ancestor is .ForeignKey, so this should match
        assert is_field_type(func_node, (".ForeignKey",)) is True

    def test_inferred_subclass_no_string_fallback_match(self):
        """A subclass with a different name should match via inference but not string fallback."""
        code = """
class ForeignKey:
    pass

class CustomRelation(ForeignKey):
    pass

class MyModel(object):
    field = CustomRelation()
"""
        func_node = _get_func_node(code)
        # "CustomRelation" wouldn't match string fallback for "ForeignKey",
        # but inference finds ForeignKey as an ancestor
        assert is_field_type(func_node, (".ForeignKey",)) is True

    def test_inferred_unrelated_subclass(self):
        """A subclass of something unrelated should not match."""
        code = """
class SomeBase:
    pass

class CustomField(SomeBase):
    pass

class MyModel(object):
    field = CustomField()
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, (".ForeignKey",)) is False


class TestIsFieldTypeMultipleFieldNames:
    """Tests with different sets of field names."""

    def test_matches_first_in_set(self):
        code = """
class MyModel:
    field = ForeignKey("SomeModel")
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, FOREIGN_KEY_QNAMES) is True

    def test_matches_second_in_set(self):
        code = """
class MyModel:
    field = OneToOneField("SomeModel")
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, FOREIGN_KEY_QNAMES) is True

    def test_single_field_name(self):
        code = """
class MyModel:
    field = ForeignKey("SomeModel")
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, ("django.db.models.fields.related.ForeignKey",)) is True

    def test_single_field_name_no_match(self):
        code = """
class MyModel:
    field = OneToOneField("SomeModel")
"""
        func_node = _get_func_node(code)
        assert is_field_type(func_node, ("django.db.models.fields.related.ForeignKey",)) is False
