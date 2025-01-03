"""Define constants for the pylint-nautobot plugin."""

from pylint.typing import MessageDefinitionTuple


class MSGS:
    """Message definitions for the pylint-nautobot plugin."""

    E4211: dict[str, MessageDefinitionTuple] = {
        "E4211": (
            "Imports a model that has been replaced (dcim.DeviceRole -> extras.Role).",
            "nb-replaced-device-role",
            "Reference: https://docs.nautobot.com/projects/core/en/next/development/apps/migration/model-updates/extras/#replace-role-related-models-with-generic-role-model",
        ),
    }
    E4212: dict[str, MessageDefinitionTuple] = {
        "E4212": (
            "Imports a model that has been replaced (dcim.RackRole -> extras.Role).",
            "nb-replaced-rack-role",
            "Reference: https://docs.nautobot.com/projects/core/en/next/development/apps/migration/model-updates/extras/#replace-role-related-models-with-generic-role-model",
        ),
    }
    E4213: dict[str, MessageDefinitionTuple] = {
        "E4213": (
            "Imports a model that has been replaced (ipam.Role -> extras.Role).",
            "nb-replaced-ipam-role",
            "Reference: https://docs.nautobot.com/projects/core/en/next/development/apps/migration/model-updates/extras/#replace-role-related-models-with-generic-role-model",
        ),
    }
    E4214: dict[str, MessageDefinitionTuple] = {
        "E4214": (
            "Imports a model that has been replaced (dcim.Region -> dcim.Location).",
            "nb-replaced-region",
            "Reference: https://docs.nautobot.com/projects/core/en/next/development/apps/migration/model-updates/dcim/#replace-site-and-region-with-location-model",
        ),
    }
    E4215: dict[str, MessageDefinitionTuple] = {
        "E4215": (
            "Imports a model that has been replaced (dcim.Site -> dcim.Location).",
            "nb-replaced-site",
            "Reference: https://docs.nautobot.com/projects/core/en/next/development/apps/migration/model-updates/dcim/#replace-site-and-region-with-location-model",
        ),
    }
    E4216: dict[str, MessageDefinitionTuple] = {
        "E4216": (
            "Imports a model that has been replaced (ipam.Aggregate -> ipam.Prefix).",
            "nb-replaced-aggregate",
            "Reference: https://docs.nautobot.com/projects/core/en/next/development/apps/migration/model-updates/ipam/#replace-aggregate-with-prefix",
        ),
    }
    E4242: dict[str, MessageDefinitionTuple] = {
        "E4242": (
            "Uses incorrect base classes (%s -> %s).",
            "nb-incorrect-base-class",
            "All classes should inherit from the correct base classes.",
        )
    }
    E4251: dict[str, MessageDefinitionTuple] = {
        "E4251": (
            "Import location has changed (%s -> %s).",
            "nb-code-location-changed",
            "Reference: https://docs.nautobot.com/projects/core/en/next/development/apps/migration/code-updates/",
        ),
    }
    E4252: dict[str, MessageDefinitionTuple] = {
        "E4252": (
            "Import location has changed for %s (%s -> %s).",
            "nb-code-location-changed-object",
            "Reference: https://docs.nautobot.com/projects/core/en/next/development/apps/migration/code-updates/",
        ),
    }
    E4261: dict[str, MessageDefinitionTuple] = {
        "E4261": (
            "Uses bad parameter combination for TextField/CharField.",
            "nb-string-field-blank-null",
            'Don\'t use blank=true and null=true on TextField or CharField. \
             It avoids confusion between a value of None and a value of ""\
             potentially having different meanings.',
        ),
    }
    E4271: dict[str, MessageDefinitionTuple] = {
        "E4271": (
            "Use `fields = '__all__'` instead of specifying each field individually.",
            "nb-use-fields-all",
            "Defining `fields = '__all__'` in a model serializer's Meta class is a Django convention that automatically "
            "includes all fields from the associated model. This approach is more maintainable because it avoids having "
            "to explicitly list each field, reducing the risk of errors and inconsistencies when the model is updated.",
        ),
    }
    C4272: dict[str, MessageDefinitionTuple] = {
        "C4272": (
            "Use `q = SearchFilter` instead of django_filters.CharFilter and the custom `search` function.",
            "nb-no-char-filter-q",
            "Nautobot provides a `SearchFilter` class that uses MappedPredicates to provide a more flexible search experience. "
            "This should be used in place of `django_filters.CharFilter` and no longer requires the custom `search` function.",
        ),
    }
    C4273: dict[str, MessageDefinitionTuple] = {
        "C4273": (
            "Use `q = SearchFilter` instead.",
            "nb-use-search-filter",
            "Nautobot provides a `SearchFilter` class that uses MappedPredicates to provide a more flexible search experience. "
            "This can be disabled if you need to use a custom Filter.",
        ),
    }
    C4274: dict[str, MessageDefinitionTuple] = {
        "C4274": (
            "Don't use custom `search` function, use SearchFilter instead.",
            "nb-no-search-function",
            "Nautobot provides a `SearchFilter` class that uses MappedPredicates to provide a more flexible search experience. "
            "This should be used in place of the custom `search` function.",
        ),
    }
    E4292: dict[str, MessageDefinitionTuple] = {
        "E4292": (
            "Inherits from the deprecated StatusModel instead of declaring status on the model explicitly with StatusField",
            "nb-status-field-instead-of-status-model",
            "Reference: https://docs.nautobot.com/projects/core/en/next/user-guide/platform-functionality/status/#status-internals",
        ),
    }
    C4701: dict[str, MessageDefinitionTuple] = {
        "C4701": (
            "Model's 'app_label.model_name' should be retrieved with 'model._meta.label_lower'",
            "nb-used-model-label-construction",
            "Replace f-string '{model._meta.app_label}.{model._meta.model}' with '{model._meta.label_lower}'.",
        ),
    }
    E4281: dict[str, MessageDefinitionTuple] = {
        "E4281": (
            "Sub-class name should be %s.",
            "nb-sub-class-name",
            "All classes should have a sub-class name that is <model class name><ancestor class type>.",
        ),
    }
    I4282: dict[str, MessageDefinitionTuple] = {
        "I4282": (
            "Model was not found in the class.",
            "nb-no-model-found",
            "Model was not found in the class.",
        ),
    }
