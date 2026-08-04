from nautobot.dcim.models import Interface


def reconnect_all(interfaces):
    return Interface.objects.bulk_update(interfaces, ["cable"])
