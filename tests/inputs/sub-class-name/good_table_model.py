from nautobot.apps.tables import BaseTable

from . import models


class AddressObjectTable(BaseTable):
    """Filter for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.AddressObject
