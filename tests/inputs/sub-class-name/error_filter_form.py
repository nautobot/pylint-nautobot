from nautobot.core.models.generics import PrimaryModel
from nautobot.extras.forms import NautobotFilterForm


class AddressObject(PrimaryModel):
    pass


class MyAddressObjectFilterForm(NautobotFilterForm):
    """Filter for AddressObject."""

    model = AddressObject
