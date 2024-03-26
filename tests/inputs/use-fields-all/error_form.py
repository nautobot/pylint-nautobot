from nautobot.extras.forms import NautobotModelForm


class AddressObjectSerializer(NautobotModelForm):
    """Model Form for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        fields = ("name", "description")
