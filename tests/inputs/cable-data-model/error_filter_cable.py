from nautobot.dcim.models import Interface


def get_uncabled_interfaces():
    return Interface.objects.filter(cable=None)
