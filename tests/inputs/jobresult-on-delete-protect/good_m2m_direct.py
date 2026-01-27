from django.db import models
from nautobot.core.models import BaseModel
from nautobot.extras.models import JobResult


class MyModel(BaseModel):
    job_results = models.ManyToManyField(JobResult)
