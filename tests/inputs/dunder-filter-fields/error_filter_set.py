from nautobot.apps.filters import MultiValueCharFilter, NautobotFilterSet


class ValidNameFilterFilterSet(NautobotFilterSet):
    """Filter for AddressObject."""

    serial__number = MultiValueCharFilter(
        lookup_expr="icontains",
        label="Serial Number",
    )
