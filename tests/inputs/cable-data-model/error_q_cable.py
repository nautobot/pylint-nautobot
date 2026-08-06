from django.db.models import Q
from nautobot.dcim.models import Interface


def get_cabled_interfaces(cable):
    return Interface.objects.filter(Q(cable=cable))
