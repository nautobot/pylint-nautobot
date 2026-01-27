from django.db import models
from django.db.models import PROTECT
from nautobot.core.models import BaseModel


class MyModel(BaseModel):
    job_result = models.OneToOneField("JobResult", on_delete=PROTECT)
