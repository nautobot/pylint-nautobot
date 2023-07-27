from django.db.models import CharField
from nautobot.core.models import BaseModel


class MyModel(BaseModel):
    name = CharField(blank=True, null=True)
