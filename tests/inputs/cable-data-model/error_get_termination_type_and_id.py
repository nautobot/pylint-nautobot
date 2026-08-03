from nautobot.dcim.models import Cable


def get_cable(interface_ct, interface):
    return Cable.objects.get(termination_a_type=interface_ct, termination_a_id=interface.pk)
