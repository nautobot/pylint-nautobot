from nautobot.dcim.models import Interface


def connect(cable):
    """The target infers to a CableTermination subclass, so this is a confirmed failure."""
    interface = Interface()
    interface.cable = cable
