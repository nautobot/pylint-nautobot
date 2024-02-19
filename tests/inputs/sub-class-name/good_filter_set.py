from nautobot.apps.filters import NautobotFilterSet
from nautobot.core.models.generics import PrimaryModel


class AddressObject(PrimaryModel):
    pass


class AddressObjectFilterSet(NautobotFilterSet):
    """Filter for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        model = AddressObject
