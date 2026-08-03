from nautobot.dcim.models import Interface


def get_interfaces_by_cable():
    return Interface.objects.all().order_by("-cable")
