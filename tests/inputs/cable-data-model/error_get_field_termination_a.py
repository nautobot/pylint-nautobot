from nautobot.dcim.models import Cable


def get_termination_field():
    """`termination_a` is now a property, so `get_field` raises FieldDoesNotExist."""
    return Cable._meta.get_field("termination_a")
