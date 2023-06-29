# Incorrect Base Classes

The following linters are defined for checking the use of Base Classes outside
of those provided by Nautobot:

## nautobot-incorrect-base-class

Looks for use of Django class type inheritance, and reports when a non-Nautobot
class is being inherited from. For example,

```python
from django.db import models


class NautobotAppModel(models.Model):
    name = models.Charfield(max_length=25)
```

will error with a message that the NautobotAppModel uses a non-Nautobot base
class.

```shell
pylint nautobot_app/ \
  --rcfile=pyproject.toml \
  --disable=all \
  --enable=nautobot-incorrect-base-class

************* Module nautobot_app.models
nautobot_app/models.py:4:0: E4242: Uses incorrect base classes.
(nb-incorrect-base-class)

... output trimmed ...
```

!!! note
    `nautobot-incorrect-base-class` can be used to include all linters provided
    below.
