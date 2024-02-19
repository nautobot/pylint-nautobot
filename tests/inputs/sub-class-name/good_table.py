from nautobot.apps.tables import BaseTable
from nautobot.core.models.generics import PrimaryModel


class AddressObject(PrimaryModel):
    pass


class AddressObjectTable(BaseTable):
    """Filter for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        model = AddressObject
