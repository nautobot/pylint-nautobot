from nautobot.apps.api import NautobotModelSerializer
from nautobot.core.models.generics import PrimaryModel


class AddressObject(PrimaryModel):
    pass


class MyAddressObjectSerializer(NautobotModelSerializer):
    """Serializer for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        model = AddressObject
