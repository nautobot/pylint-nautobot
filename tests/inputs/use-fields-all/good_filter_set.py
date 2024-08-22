from nautobot.apps.filters import NautobotFilterSet


class AddressObjectFilterSet(NautobotFilterSet):
    """Filter for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        fields = "__all__"
