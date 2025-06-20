from nautobot.apps.filters import NautobotFilterSet, SearchFilter


class ValidNameFilterFilterSet(NautobotFilterSet):
    """Filter for AddressObject."""

    q__name = SearchFilter(
        filter_predicates={
            "name": ["name__icontains"],
            "description": ["description__icontains"],
        }
    )
