from nautobot.apps.filters import MultiValueCharFilter, NautobotFilterSet


class ValidNameFilterFilterSet(NautobotFilterSet):
    """Filter for AddressObject."""

    serial_number = MultiValueCharFilter(
        lookup_expr="icontains",
        label="Serial Number",
    )
