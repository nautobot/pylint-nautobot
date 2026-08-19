from nautobot.dcim.models import Interface


def get_interfaces():
    return Interface.objects.all().select_related("cable__status")
