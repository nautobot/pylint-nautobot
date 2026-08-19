from nautobot.dcim.models import Interface


def get_cable_field():
    """`cable` is now a property, so `get_field` raises FieldDoesNotExist."""
    return Interface._meta.get_field("cable")
