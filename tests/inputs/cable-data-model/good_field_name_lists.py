from nautobot.dcim.models import Interface


def save_unrelated_fields(interface):
    """Field-name collections that name surviving fields are fine."""
    interface.save(update_fields=["name", "description"])
    interface.refresh_from_db(fields=["cable_termination"])
    return Interface.objects.bulk_update([interface], ["description"])


def save_everything(interface):
    """A `save()` with no `update_fields` names no fields at all."""
    interface.save()
