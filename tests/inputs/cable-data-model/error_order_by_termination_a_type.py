from nautobot.dcim.models import Cable


def get_cables():
    return Cable.objects.all().order_by("termination_a_type")
