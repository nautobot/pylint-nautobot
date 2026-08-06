from django.db.models import Q
from nautobot.dcim.models import Cable


def get_cables(interface):
    return Cable.objects.filter(Q(terminations__interface_id=interface.pk, terminations__cable_end="A"))


def get_other_cables(interface, front_port):
    return Cable.objects.exclude(terminations__interface_id=interface.pk).exclude(
        terminations__front_port_id=front_port.pk
    )
