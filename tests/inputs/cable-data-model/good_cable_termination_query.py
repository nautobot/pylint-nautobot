from django.db.models import Q
from nautobot.dcim.models import Interface


def get_cabled_interfaces(cable):
    return (
        Interface.objects.filter(Q(cable_termination__cable=cable))
        .select_related("cable_termination__cable")
        .order_by("cable_termination__cable")
    )


def get_uncabled_interfaces():
    return Interface.objects.filter(cable_termination__isnull=True)
