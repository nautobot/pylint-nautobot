def reload(interface):
    interface.refresh_from_db(fields=["cable"])
