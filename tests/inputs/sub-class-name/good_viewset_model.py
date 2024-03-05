from nautobot.apps.views import NautobotUIViewSet

from . import models


class AddressObjectUIViewSet(NautobotUIViewSet):
    """Filter for AddressObject."""

    queryset = models.AddressObject.objects.all()
