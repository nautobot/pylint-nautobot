from nautobot.dcim.models import FrontPort


def get_cable_pks():
    return FrontPort.objects.all().values_list("cable", flat=True)
