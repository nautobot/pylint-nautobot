from nautobot.apps.views import NautobotUIViewSet
from nautobot.core.models.generics import PrimaryModel


class AddressObject(PrimaryModel):
    pass


class AddressObjectUIViewSet(NautobotUIViewSet):
    """Filter for AddressObject."""

    queryset = AddressObject.objects.all()
