from django.db.models import Q
from nautobot.apps.filters import NautobotFilterSet


class MissingQFilterFilterSet(NautobotFilterSet):
    """Filter for AddressObject."""

    def search(self, queryset, name, value):
        """Search for a string in multiple fields."""
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))
