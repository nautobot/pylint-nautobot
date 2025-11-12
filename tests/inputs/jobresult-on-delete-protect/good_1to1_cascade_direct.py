from django.db import models
from nautobot.core.models import BaseModel
from nautobot.extras.models import JobResult


class MyModel(BaseModel):
    job_result = models.OneToOneField(JobResult, on_delete=models.CASCADE)
