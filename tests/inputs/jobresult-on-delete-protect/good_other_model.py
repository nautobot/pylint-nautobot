from django.db import models
from nautobot.core.models import BaseModel
from nautobot.extras.models import Status


class MyModel(BaseModel):
    # This should not trigger because it's not JobResult
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    # This should not trigger because it's not JobResult
    other_job = models.ForeignKey("extras.Job", on_delete=models.SET_NULL)
