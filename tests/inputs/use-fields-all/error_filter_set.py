from nautobot.apps.filters import NautobotFilterSet


class MyAddressObjectFilterSet(NautobotFilterSet):
    """Filter for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        fields = ("name", "description")
