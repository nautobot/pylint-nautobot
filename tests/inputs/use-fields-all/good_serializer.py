from nautobot.apps.api import NautobotModelSerializer


class AddressObjectSerializer(NautobotModelSerializer):
    """Serializer for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        fields = "__all__"
