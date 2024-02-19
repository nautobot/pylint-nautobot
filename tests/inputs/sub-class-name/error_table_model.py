from nautobot.apps.tables import BaseTable

from . import models


class MyAddressObjectTable(BaseTable):
    """Filter for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.AddressObject
