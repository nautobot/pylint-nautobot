from nautobot.dcim.models import Cable


def get_or_create_cable(interface, status):
    return Cable.objects.get_or_create(termination_a_id=interface.pk, defaults={"status": status})
