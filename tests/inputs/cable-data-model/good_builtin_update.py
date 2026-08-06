def build_defaults(cable, interface):
    """A dict receiver is provably not a queryset, so its keywords are ordinary keys."""
    defaults = {}
    defaults.update(cable=cable, termination_a_id=interface.pk)
    return defaults
