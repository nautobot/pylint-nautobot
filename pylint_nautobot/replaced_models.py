"""Check for usage of models that were replaced in 2.0."""
from typing import Optional

import importlib_resources

import yaml

from astroid import AssignName, Call, nodes

from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


with open(
    importlib_resources.files("pylint_nautobot").joinpath("data/v2/v2-database-replaced-models.yaml"), encoding="utf-8"
) as fh:
    V2_REPLACED_MODELS = yaml.safe_load(fh)


RELATIONSHIP_CLASS_NAMES = {"ForeignKey", "ManyToManyField", "OneToOneField"}


class NautobotReplacedModelsImportChecker(BaseChecker):
    """Visit 'import from' statements to find usage of models that have been replaced in 2.0."""

    __implements__ = IAstroidChecker

    version_specifier = ">=2,<3"

    name = "nautobot-replaced-models"
    msgs = {
        "E4211": (
            "Imports a model that has been replaced (dcim.DeviceRole -> extras.Role).",
            "nb-replaced-device-role",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#generic-role-model",
        ),
        "E4212": (
            "Imports a model that has been replaced (dcim.RackRole -> extras.Role).",
            "nb-replaced-rack-role",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#generic-role-model",
        ),
        "E4213": (
            "Imports a model that has been replaced (ipam.Role -> extras.Role).",
            "nb-replaced-ipam-role",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#generic-role-model",
        ),
        "E4214": (
            "Imports a model that has been replaced (dcim.Region -> dcim.Location).",
            "nb-replaced-region",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#site-and-region-models",
        ),
        "E4215": (
            "Imports a model that has been replaced (dcim.Site -> dcim.Location).",
            "nb-replaced-site",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#site-and-region-models",
        ),
        "E4216": (
            "Imports a model that has been replaced (ipam.Aggregate -> ipam.Prefix).",
            "nb-replaced-aggregate",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#aggregate-migrated-to-prefix",
        ),
    }

    def visit_importfrom(self, node):
        if node.modname == "nautobot.dcim.models":
            for name, _ in node.names:
                if name == "DeviceRole":
                    self.add_message("nb-replaced-device-role", node=node)
                elif name == "RackRole":
                    self.add_message("nb-replaced-rack-role", node=node)
                elif name == "Region":
                    self.add_message("nb-replaced-region", node=node)
                elif name == "Site":
                    self.add_message("nb-replaced-site", node=node)
        if node.modname == "nautobot.ipam.models":
            for name, _ in node.names:
                if name == "Role":
                    self.add_message("nb-replaced-ipam-role", node=node)
                elif name == "Aggregate":
                    self.add_message("nb-replaced-aggregate", node=node)


class NautobotReplacedModelsRelatedObjectChecker(BaseChecker):
    """Visit Model field definitions to find usage of models that have been replaced.

    This iterates through class attributes looking for instantiation of foriegn
    key class fields, and verifies that the relation is not assigned to a
    Nautobot Model that has been replaced.
    """

    __implements__ = IAstroidChecker

    version_specifier = ">=2,<3"

    name = "nautobot-replaced-models-related-object-fields"
    msgs = {
        "E4311": (
            "Related object field is related to a model that has been replaced (%s -> %s).",
            "nb-replaced-model-related-object-field",
            "https://docs.nautobot.com/projects/core/en/next/installation/upgrading-from-nautobot-v1/#replaced-models",
        ),
    }

    @staticmethod
    def _get_related_model(relationship_field: Call) -> Optional[str]:
        """Get app.Model of related object."""
        # Check if args were passed
        if relationship_field.args:
            # The `to` arg is the first argument
            return relationship_field.args[0].value
        # Check keyword args if args were not passed
        for keyword in relationship_field.keywords:
            if keyword.arg == "to":
                return keyword.value.value

        # Check kwargs as a last resort
        for kwargs in relationship_field.kwargs:
            # `relationship_field.kwargs` is a list of `Keyword` instances
            for kwarg in kwargs.value.items:
                # `kwargs.value.items` is a list of key,value tuples
                if kwarg[0].value == "to":
                    return kwarg[1].value

        # Unable to find the model that is being related to
        return None

    def visit_classdef(self, node: nodes.ClassDef) -> None:
        """Reports related object fields that use a model that has been replaced."""
        relationship_fields = [
            value.assign_type().value
            for value in node.values()
            # Filters out things like method definitions
            if isinstance(value, AssignName)
            # Filters out attrs that are not assigned callables
            and isinstance(value.assign_type().value, Call)
            # Filters out non relationship fields
            and value.assign_type().value.func.attrname in RELATIONSHIP_CLASS_NAMES
        ]

        related_model = None
        for relationship_field in relationship_fields:
            related_model = self._get_related_model(relationship_field)
            if related_model is None:
                continue  # Relationship cannot not be determined, so ignore

            try:
                app, model = related_model.split(".")
            except ValueError:
                continue  # App/Model cannot be determined, so ignore

            replaced_app = V2_REPLACED_MODELS.get(app, {})
            replaced_model = replaced_app.get(model)
            # Only log an error when Model has been replaced
            if replaced_model:
                replaced_app_model = f"{replaced_model['new_app']}.{replaced_model['new_model']}"
                self.add_message(
                    "nb-replaced-model-related-object-field",
                    node=node,
                    args=(related_model, replaced_app_model),
                )
