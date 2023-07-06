"""Unittests for code in pylint_nautobot/replaced_models.py."""
# pylint: disable=protected-access
from unittest import mock

import pytest
from pylint.testutils import CheckerTestCase

import astroid

from pylint_nautobot import replaced_models


class TestNautobotReplacedModelsRelatedObjectChecker(CheckerTestCase):
    """Unittests for NautobotReplacedModelsRelatedObjectChecker class."""

    CHECKER_CLASS = replaced_models.NautobotReplacedModelsRelatedObjectChecker

    @pytest.fixture
    def checker(self):
        """Replace _extract_to_field_contents method with a mock."""
        with mock.patch.object(self.checker, "_extract_to_field_contents") as mock_extract_to_field_contents:
            self.checker._extract_to_field_contents = mock_extract_to_field_contents
            yield self.checker

    def test_extract_to_field_contents_str(self):
        expected = "dcim.Site"
        assign = astroid.extract_node(f"class MyModel(PrimaryModel):\n    fk = ForeignKey('{expected}')  #@")
        to_field = assign.value.args[0]
        actual = self.checker._extract_to_field_contents(to_field)
        assert actual == expected
        # verify path taken in function, as mocking isinstance will cause issues
        assert isinstance(to_field, astroid.Const)
        assert isinstance(to_field.value, str)

    def test_extract_to_field_contents_int(self):
        assign = astroid.extract_node("class MyModel(PrimaryModel):\n    fk = ForeignKey(1)  #@")
        to_field = assign.value.args[0]
        actual = self.checker._extract_to_field_contents(to_field)
        assert actual is None
        # verify path taken in function, as mocking isinstance will cause issues
        assert isinstance(to_field, astroid.Const)
        assert isinstance(to_field.value, int)

    def test_extract_to_field_contents_app_model(self):
        expected = "dcim.Site"
        assign = astroid.extract_node(f"class MyModel(PrimaryModel):\n    fk = ForeignKey({expected})  #@")
        to_field = assign.value.args[0]
        actual = self.checker._extract_to_field_contents(to_field)
        assert actual == expected
        # verify path taken in function, as mocking isinstance will cause issues
        assert isinstance(to_field, astroid.Attribute)

    def test_extract_to_field_contents_model(self):
        expected = "Site"
        assign = astroid.extract_node(f"class MyModel(PrimaryModel):\n    fk = ForeignKey({expected})  #@")
        to_field = assign.value.args[0]
        actual = self.checker._extract_to_field_contents(to_field)
        assert actual == expected
        # verify path taken in function, as mocking isinstance will cause issues
        assert isinstance(to_field, astroid.Name)

    def test_extract_to_field_contents_lambda(self):
        assign = astroid.extract_node("class MyModel(PrimaryModel):\n    fk = ForeignKey(lambda x: x)  #@")
        to_field = assign.value.args[0]
        actual = self.checker._extract_to_field_contents(to_field)
        assert actual is None
        # verify path taken in function, as mocking isinstance will cause issues
        assert isinstance(to_field, astroid.Lambda)

    @staticmethod
    def test_get_related_model_args(checker):
        expected = "dcim.Site"
        assign = astroid.extract_node(f"class MyModel(PrimaryModel):\n    fk = ForeignKey('{expected}')  #@")
        call = assign.value
        call.keywords = mock.Mock()
        checker._extract_to_field_contents.return_value = expected
        actual = checker._get_related_model(call)
        assert actual == expected
        call.keywords.assert_not_called()
        checker._extract_to_field_contents.assert_called_with(call.args[0])

    @staticmethod
    def test_get_related_model_keywords(checker):
        expected = "dcim.Site"
        assign = astroid.extract_node(f"class MyModel(PrimaryModel):\n    fk = ForeignKey(to='{expected}')  #@")
        call = assign.value
        checker._extract_to_field_contents.return_value = expected
        actual = checker._get_related_model(call)
        assert actual == expected
        checker._extract_to_field_contents.assert_called_with(call.keywords[0].value)

    @staticmethod
    def test_get_related_model_kwargs(checker):
        expected = "dcim.Site"
        assign = astroid.extract_node(
            f"class MyModel(PrimaryModel):\n    fk = ForeignKey(**{{'to': '{expected}'}})  #@"
        )
        call = assign.value
        checker._extract_to_field_contents.return_value = expected
        actual = checker._get_related_model(call)
        assert actual == expected
        checker._extract_to_field_contents.assert_called_with(call.kwargs[0].value.items[0][1])

    @staticmethod
    def test_get_related_model_no_to_field(checker):
        assign = astroid.extract_node("class MyModel(PrimaryModel):\n    fk = ForeignKey(on_delete=models.CASCADE)  #@")
        call = assign.value
        actual = checker._get_related_model(call)
        assert actual is None
        checker._extract_to_field_contents.assert_not_called()
