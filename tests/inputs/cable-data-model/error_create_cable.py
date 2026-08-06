from nautobot.dcim.models import Interface


def create_interface(device, cable):
    return Interface.objects.create(device=device, name="Ethernet1/1", cable=cable)
