def disconnect(interface):
    """Reading `.cable` still works, and assigning `None` is the supported way to disconnect."""
    if interface.cable is not None:
        interface.cable = None
        interface.save()
    return interface.get_cable_peer()
