from nautobot.apps.views import NautobotUIViewSet

from . import models


class MyAddressObjectUIViewSet(NautobotUIViewSet):
    """Filter for AddressObject."""

    queryset = models.AddressObject.objects.all()
