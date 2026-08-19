from nautobot.dcim.models import Interface


def get_connected_interfaces():
    return Interface.objects.filter(cable_paths__is_active=True).distinct()


def get_endpoints(interface):
    return interface.get_connected_endpoints()
