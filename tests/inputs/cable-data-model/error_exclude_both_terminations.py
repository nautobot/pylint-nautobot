from nautobot.dcim.models import Cable


def get_other_cables(interface, front_port):
    return Cable.objects.exclude(termination_a_id=interface.pk, termination_b_id=front_port.pk)
