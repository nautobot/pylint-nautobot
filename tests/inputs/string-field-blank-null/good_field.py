from django.db import models
from django.db.models import CharField
from nautobot.core.models import BaseModel

class MyModelOne(BaseModel):
    name = CharField(blank=True)


class MyModelTwo(BaseModel):
    name = CharField(null=True)

class MyModelThree(BaseModel):
    name = models.TextField(null=True)
