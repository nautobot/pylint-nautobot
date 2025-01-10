import django_filters
from nautobot.apps.filters import NautobotFilterSet


class IncorrectQFilterTypeFilterSet(NautobotFilterSet):
    """Filter for AddressObject."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
