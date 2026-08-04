def disconnect(interface):
    interface.save(update_fields=["name", "cable"])
