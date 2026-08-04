from django.db.models import FilteredRelation, Q
from nautobot.dcim.models import Interface


def annotate_connected_cable():
    return Interface.objects.annotate(connected=FilteredRelation("cable", condition=Q(name="Ethernet1/1")))
