from nautobot.core.models.generics import PrimaryModel
from nautobot.extras.forms import NautobotFilterForm


class AddressObject(PrimaryModel):
    pass


class AddressObjectFilterForm(NautobotFilterForm):
    """Filter for AddressObject."""

    model = AddressObject
