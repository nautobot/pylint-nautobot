# Code Location Changes

The following linters are defined for checking import statements that use
`from...import` syntax and have moved in different versions of Nautobot:


## nb-code-location-changes

Looks for imports using Nautobot modules that have been moved. For example,

```python
from nautobot.utilities.fields import NullableCharField
```

will error with a message that the fields module has been moved to
`nautobot.core.models.fields`.

```shell
pylint nautobot_app/ \
  --rcfile=pyproject.toml \
  --disable=all \
  --enable=nautobot-code-location-changes

************* Module nautobot_app.fields
nautobot_app/fields.py:3:0: E4251: Import location has changed
(nautobot.utilities.fields -> nautobot.core.models.fields).
(nb-code-location-changed)

... output trimmed ...
```

## nb-code-location-changed-object

Looks for imports of Nauotobt objects that have been moved. For example,

```python
from nautobot.utilities.utils import csv_format
```

will error with a message that the csv_format function has moved to
`nautobot.core.views.utils`.

```shell
pylint nautobot_app/ \
  --rcfile=pyproject.toml \
  --disable=all \
  --enable=nautobot-code-location-changes

************* Module nautobot_app.views
nautobot_app/views.py:3:0: E4252: Import location has changed for
csv_format (nautobot.utilities.utils -> nautobot.core.views.utils).
(nb-code-location-changed-object)

... output trimmed ...
```

!!! note
    `nautobot-code-location-changes` can be used to include all linters provided
    below.