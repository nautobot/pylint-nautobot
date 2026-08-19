from nautobot.dcim.models import Interface


def get_connected_interfaces():
    return Interface.objects.filter(_path__is_active=True)
