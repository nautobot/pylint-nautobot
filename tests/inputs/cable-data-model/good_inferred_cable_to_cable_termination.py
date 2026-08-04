from nautobot.dcim.models import CableToCableTermination


def reassign(cable):
    """A local holding a join model record: recognised by inferring its type, not by its name.

    `CableToCableTermination` is new in Nautobot 3.2, so astroid can only resolve this on 3.2 and later, which is
    why this fixture is version gated.
    """
    row = CableToCableTermination()
    row.cable = cable
    return row
