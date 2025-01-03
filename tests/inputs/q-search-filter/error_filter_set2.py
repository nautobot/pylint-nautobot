from nautobot.apps.filters import NautobotFilterSet, SearchFilter


class CustomSearchFilter(SearchFilter):
    """Custom search filter."""

    filter_predicates = {
        "name": ["name__icontains"],
        "description": ["description__icontains"],
    }


class MyAddressObjectFilterSet(NautobotFilterSet):
    """Filter for AddressObject."""

    q = CustomSearchFilter()
