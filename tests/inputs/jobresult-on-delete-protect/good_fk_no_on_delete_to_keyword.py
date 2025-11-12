from django.db import models
from nautobot.core.models import BaseModel


class MyModel(BaseModel):
    job_result = models.ForeignKey(to="extras.JobResult")
