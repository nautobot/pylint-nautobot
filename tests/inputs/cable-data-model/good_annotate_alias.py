from django.db.models import Count
from nautobot.dcim.models import Interface


def annotate_alias():
    """The `annotate`/`aggregate`/`alias` keyword is a caller-invented output alias, not a field reference."""
    return Interface.objects.annotate(cable=Count("pk")).alias(cable_id=Count("pk"))


def aggregate_alias():
    return Interface.objects.aggregate(cable=Count("pk"))
