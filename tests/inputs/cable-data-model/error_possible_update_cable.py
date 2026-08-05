def build_defaults(defaults, cable):
    """`update()` is a queryset method and a dict method; nothing here identifies which this is."""
    defaults.update(cable=cable)
