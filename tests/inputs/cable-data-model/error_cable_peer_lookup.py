from nautobot.dcim.models import Interface


def get_interfaces_by_peer_type(content_type):
    return Interface.objects.filter(_cable_peer_type=content_type)
