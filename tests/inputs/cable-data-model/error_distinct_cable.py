from nautobot.dcim.models import Interface


def get_one_interface_per_cable():
    return Interface.objects.order_by("cable_termination__cable").distinct("cable")
