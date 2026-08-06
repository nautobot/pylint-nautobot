from nautobot.dcim.models import Cable


def connect(interface, front_port, status):
    cable = Cable.objects.create(termination_a=interface, termination_b=front_port, status=status)
    cable.add_termination(front_port, "B", connector=2)
    return cable
