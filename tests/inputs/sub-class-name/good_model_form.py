from nautobot.core.models.generics import PrimaryModel
from nautobot.extras.forms import NautobotModelForm


class AddressObject(PrimaryModel):
    pass


class AddressObjectForm(NautobotModelForm):
    """Filter for AddressObject."""

    class Meta:
        """Meta attributes."""

        model = AddressObject
