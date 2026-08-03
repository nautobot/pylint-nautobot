from nautobot.dcim.models import CableToCableTermination


def get_a_side(cable):
    """`CableToCableTermination` has real `cable`/`cable_id` fields, so these lookups are already correct."""
    return CableToCableTermination.objects.filter(cable=cable, cable_end="A").select_related("cable")


def get_cable_pks(interfaces):
    return CableToCableTermination.objects.filter(interface__in=interfaces).values_list("cable_id", flat=True)


def add_termination(cable, interface):
    return CableToCableTermination.objects.create(cable=cable, cable_end="A", interface=interface)


def get_connectors(cable):
    return cable.terminations.values("cable_id", "connector")
