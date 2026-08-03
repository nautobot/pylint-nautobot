from nautobot.dcim.models import Cable


def get_cables(interface):
    return Cable.objects.filter(termination_a_id=interface.pk)
