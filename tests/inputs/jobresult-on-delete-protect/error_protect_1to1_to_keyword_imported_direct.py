from django.db import models
from django.db.models import PROTECT
from nautobot.core.models import BaseModel
from nautobot.extras.models import JobResult


class MyModel(BaseModel):
    job_result = models.OneToOneField(to=JobResult, on_delete=PROTECT)
