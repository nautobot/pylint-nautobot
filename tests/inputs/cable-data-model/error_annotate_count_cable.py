from django.db.models import Count
from nautobot.dcim.models import Interface


def count_cables():
    """The field reference lives in the value, not the keyword."""
    return Interface.objects.annotate(num=Count("cable"))
