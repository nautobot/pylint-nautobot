from nautobot.dcim.models import Cable


def get_oldest_cable():
    return Cable.objects.earliest("termination_a_id")
