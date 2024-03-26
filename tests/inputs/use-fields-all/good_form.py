from nautobot.extras.forms import NautobotModelForm


class AddressObjectSerializer(NautobotModelForm):
    """Model Form for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        fields = "__all__"
