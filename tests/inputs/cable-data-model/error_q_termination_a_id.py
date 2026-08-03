from django.db.models import Q
from nautobot.dcim.models import Cable


def get_cables(interface):
    return Cable.objects.filter(Q(termination_a_id=interface.pk))
