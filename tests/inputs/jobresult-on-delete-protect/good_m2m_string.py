from django.db import models
from nautobot.core.models import BaseModel


class MyModel(BaseModel):
    job_results = models.ManyToManyField("extras.JobResult")
