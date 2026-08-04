from nautobot.dcim.models import Interface


def get_newest_cabled_interface():
    return Interface.objects.latest("cable")
