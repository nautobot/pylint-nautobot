from django.db import models
from django.db.models import CASCADE
from nautobot.core.models import BaseModel


class MyModel(BaseModel):
    job_result = models.ForeignKey("extras.JobResult", on_delete=CASCADE)
