from django.db import models

from nautobot.core.models.generics import PrimaryModel


class MyModel(PrimaryModel):
    dcim_device_role = models.ForeignKey("dcim.DeviceRole")
    dcim_rack_role = models.ManyToManyField(to="dcim.RackRole")
    dcim_region = models.OneToOneField(**{"to": "dcim.Region"})
    dcim_site = models.ForeignKey("dcim.Site")
    ipam_aggregate = models.ForeignKey("ipam.Aggregate")
    ipam_role = models.ForeignKey("ipam.Role")
