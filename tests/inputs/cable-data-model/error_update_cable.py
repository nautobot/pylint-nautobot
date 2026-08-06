from nautobot.dcim.models import Interface


def disconnect_all(device):
    """Unlike `termination.cable = None`, `update()` resolves against real fields and raises FieldDoesNotExist."""
    return Interface.objects.filter(device=device).update(cable=None)
