def connect(interface, cable):
    interface.cable = cable
    interface.save()
