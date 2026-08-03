from nautobot.dcim.models import Cable


def get_cables(interface_pks):
    return Cable.objects.filter(termination_a_id__in=interface_pks)
