from nautobot.apps.filters import NautobotFilterSet, SearchFilter


class ValidQFilterFilterSet(NautobotFilterSet):
    """Filter for AddressObject."""

    q = SearchFilter(
        filter_predicates={
            "name": ["name__icontains"],
            "description": ["description__icontains"],
        }
    )
