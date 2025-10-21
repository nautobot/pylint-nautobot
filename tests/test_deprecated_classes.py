"""Tests for deprecated classes checker."""

from pylint.testutils import CheckerTestCase

from pylint_nautobot.deprecated_classes import NautobotDeprecatedClassChecker

from .utils import (
    assert_error_file,
    assert_good_file,
    parametrize_error_files,
    parametrize_good_files,
)

_BASE_ERROR = {
    "versions": ">=2",
    "msg_id": "nb-deprecated-class",
    "line": 4,
    "end_line": 4,
    "col_offset": 0,
    "node": lambda module_node: module_node.body[1],
}

_EXPECTED_ERRORS = {
    "device_component_filter_set": {
        **_BASE_ERROR,
        "end_col_offset": 17,
        "args": (
            "nautobot.dcim.filters.DeviceComponentFilterSet",
            "nautobot.dcim.filters.mixins.DeviceComponentModelFilterSetMixin",
        ),
    },
    "device_type_component_filter_set": {
        **_BASE_ERROR,
        "end_col_offset": 17,
        "args": (
            "nautobot.dcim.filters.DeviceTypeComponentFilterSet",
            "nautobot.dcim.filters.mixins.DeviceComponentTemplateModelFilterSetMixin",
        ),
    },
    "cable_termination_filter_set": {
        **_BASE_ERROR,
        "end_col_offset": 17,
        "args": (
            "nautobot.dcim.filters.CableTerminationFilterSet",
            "nautobot.dcim.filters.mixins.CableTerminationModelFilterSetMixin",
        ),
    },
    "path_endpoint_filter_set": {
        **_BASE_ERROR,
        "end_col_offset": 17,
        "args": (
            "nautobot.dcim.filters.PathEndpointFilterSet",
            "nautobot.dcim.filters.mixins.PathEndpointModelFilterSetMixin",
        ),
    },
    "connection_filter_set": {
        **_BASE_ERROR,
        "end_col_offset": 17,
        "args": (
            "nautobot.dcim.filters.ConnectionFilterSet",
            "nautobot.dcim.filters.ConnectionFilterSetMixin",
        ),
    },
    "cable_termination_serializer": {
        **_BASE_ERROR,
        "end_col_offset": 18,
        "args": (
            "nautobot.dcim.api.serializers.CableTerminationSerializer",
            "nautobot.dcim.api.serializers.CableTerminationModelSerializerMixin",
        ),
    },
    "connected_endpoint_serializer": {
        **_BASE_ERROR,
        "end_col_offset": 18,
        "args": (
            "nautobot.dcim.api.serializers.ConnectedEndpointSerializer",
            "nautobot.dcim.api.serializers.PathEndpointModelSerializerMixin",
        ),
    },
    "created_updated_filter_set": {
        **_BASE_ERROR,
        "end_col_offset": 17,
        "args": (
            "nautobot.extras.filters.CreatedUpdatedFilterSet",
            "nautobot.extras.filters.mixins.CreatedUpdatedModelFilterSetMixin",
        ),
    },
    "relationship_model_filter_set": {
        **_BASE_ERROR,
        "end_col_offset": 17,
        "args": (
            "nautobot.extras.filters.RelationshipModelFilterSet",
            "nautobot.extras.filters.mixins.RelationshipModelFilterSetMixin",
        ),
    },
    "custom_field_model_filter_set": {
        **_BASE_ERROR,
        "end_col_offset": 17,
        "args": (
            "nautobot.extras.filters.CustomFieldModelFilterSet",
            "nautobot.extras.filters.mixins.CustomFieldModelFilterSetMixin",
        ),
    },
    "local_context_filter_set": {
        **_BASE_ERROR,
        "end_col_offset": 17,
        "args": (
            "nautobot.extras.filters.LocalContextFilterSet",
            "nautobot.extras.filters.mixins.LocalContextModelFilterSetMixin",
        ),
    },
    "custom_field_bulk_create_form": {
        **_BASE_ERROR,
        "end_col_offset": 12,
        "args": (
            "nautobot.extras.forms.forms.CustomFieldBulkCreateForm",
            "nautobot.extras.forms.mixins.CustomFieldBulkCreateForm",
        ),
    },
    "add_remove_tags_form": {
        **_BASE_ERROR,
        "end_col_offset": 12,
        "args": (
            "nautobot.extras.forms.mixins.AddRemoveTagsForm",
            "nautobot.extras.forms.mixins.TagsBulkEditFormMixin",
        ),
    },
    "custom_field_bulk_edit_form": {
        **_BASE_ERROR,
        "end_col_offset": 12,
        "args": (
            "nautobot.extras.forms.mixins.CustomFieldBulkEditForm",
            "nautobot.extras.forms.mixins.CustomFieldModelBulkEditFormMixin",
        ),
    },
    "custom_field_model_form": {
        **_BASE_ERROR,
        "end_col_offset": 12,
        "args": (
            "nautobot.extras.forms.mixins.CustomFieldModelForm",
            "nautobot.extras.forms.mixins.CustomFieldModelFormMixin",
        ),
    },
    "relationship_model_form": {
        **_BASE_ERROR,
        "end_col_offset": 12,
        "args": (
            "nautobot.extras.forms.mixins.RelationshipModelForm",
            "nautobot.extras.forms.mixins.RelationshipModelFormMixin",
        ),
    },
    "status_bulk_edit_form_mixin": {
        **_BASE_ERROR,
        "end_col_offset": 12,
        "args": (
            "nautobot.extras.forms.mixins.StatusBulkEditFormMixin",
            "nautobot.extras.forms.mixins.StatusModelBulkEditFormMixin",
        ),
    },
    "status_filter_form_mixin": {
        **_BASE_ERROR,
        "end_col_offset": 12,
        "args": (
            "nautobot.extras.forms.mixins.StatusFilterFormMixin",
            "nautobot.extras.forms.mixins.StatusModelFilterFormMixin",
        ),
    },
    "tenancy_filter_set": {
        **_BASE_ERROR,
        "end_col_offset": 17,
        "args": (
            "nautobot.tenancy.filters.TenancyFilterSet",
            "nautobot.tenancy.filters.mixins.TenancyModelFilterSetMixin",
        ),
    },
    "name_only_filter_test_case": {
        **_BASE_ERROR,
        "end_col_offset": 16,
        "args": (
            "nautobot.core.testing.filters.FilterTestCases.NameOnlyFilterTestCase",
            "nautobot.core.testing.filters.FilterTestCases.FilterTestCase",
        ),
    },
    "custom_link_button_class_choices": {
        **_BASE_ERROR,
        "end_col_offset": 15,
        "args": (
            "nautobot.extras.choices.CustomLinkButtonClassChoices",
            "nautobot.extras.choices.ButtonClassChoices",
        ),
    },
    "plugin_config": {
        **_BASE_ERROR,
        "end_col_offset": 14,
        "args": (
            "nautobot.extras.plugins.PluginConfig",
            "nautobot.extras.plugins.NautobotAppConfig",
        ),
    },
    "plugin_template_extension": {
        **_BASE_ERROR,
        "end_col_offset": 17,
        "args": (
            "nautobot.extras.plugins.PluginTemplateExtension",
            "nautobot.extras.plugins.TemplateExtension",
        ),
    },
    "plugin_banner": {
        **_BASE_ERROR,
        "end_col_offset": 14,
        "args": (
            "nautobot.extras.plugins.PluginBanner",
            "nautobot.extras.plugins.Banner",
        ),
    },
    "plugin_filter_extension": {
        **_BASE_ERROR,
        "end_col_offset": 17,
        "args": (
            "nautobot.extras.plugins.PluginFilterExtension",
            "nautobot.extras.plugins.FilterExtension",
        ),
    },
    "plugin_custom_validator": {
        **_BASE_ERROR,
        "end_col_offset": 17,
        "node": lambda module_node: module_node.body[1],
        "args": (
            "nautobot.extras.plugins.PluginCustomValidator",
            "nautobot.extras.plugins.CustomValidator",
        ),
    },
}


class TestDeprecatedClassesChecker(CheckerTestCase):
    """Test deprecated classes checker."""

    CHECKER_CLASS = NautobotDeprecatedClassChecker

    @parametrize_error_files(__file__, _EXPECTED_ERRORS)
    def test_error(self, filename, expected_error):
        assert_error_file(self, filename, expected_error)

    @parametrize_good_files(__file__)
    def test_good(self, filename):
        assert_good_file(self, filename)
