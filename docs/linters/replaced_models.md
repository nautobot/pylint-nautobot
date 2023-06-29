# Replaced Models

The following linters are defined for the use of Models that have been
superceded by other Models in newer versions of Nautobot:

!!! warning
    The linters defined below are currently only looking for imports of Models
    that have been removed. Defining a ForiegnKey field with the `to` field
    using a str of the Model's location will not currently be caught (Ex:
    role = models.ForeignKey(to="dcim.DeviceRole")).

## nb-replaced-device-role

Looks for imports of `dcim.DeviceRole` Model class to notify that this Model has
been replaced by the `extras.Role` Model. For example,

```python
from nautobot.dcim.models import DeviceRole
```

will error with a message that Nautobot's `dcim.DeviceRole` Model has been
replaced with `extras.Role`.

```shell
pylint nautobot_app/ \
  --rcfile=pyproject.toml \
  --disable=all \
  --enable="nautobot-replaced-models"

************* Module nautobot_app.models
nautobot_app/models.py:1:0: E4211: Imports a model that has been replaced
(dcim.DeviceRole -> extras.Role). (nb-replaced-device-role)

... output trimmed ...
```

## nb-replaced-rack-role

Looks for imports of `dcim.RackRole` Model class to notify that this Model has
been replaced by the `extras.Role` Model. For example,

```python
from nautobot.dcim.models import RackRole
```

will error with a message that Nautobot's `dcim.RackRole` Model has been
replaced with `extras.Role`.

```shell
pylint nautobot_app/ \
  --rcfile=pyproject.toml \
  --disable=all \
  --enable="nautobot-replaced-models"

************* Module nautobot_app.models
nautobot_app/models.py:1:0: E4211: Imports a model that has been replaced
(dcim.RackRole -> extras.Role). (nb-replaced-rack-role)

... output trimmed ...
```
## nb-replaced-ipam-role

Looks for imports of `ipam.Role` Model class to notify that this Model has
been replaced by the `extras.Role` Model. For example,

```python
from nautobot.ipam.models import Role
```

will error with a message that Nautobot's `ipam.Role` Model has been
replaced with `extras.Role`.

```shell
pylint nautobot_app/ \
  --rcfile=pyproject.toml \
  --disable=all \
  --enable="nautobot-replaced-models"

************* Module nautobot_app.models
nautobot_app/models.py:1:0: E4211: Imports a model that has been replaced
(ipam.Role -> extras.Role). (nb-replaced-ipam-role)

... output trimmed ...
```

## nb-replaced-region

Looks for imports of `dcim.Region` Model class to notify that this Model has
been replaced by the `dcim.Location` Model. For example,

```python
from nautobot.dcim.models import Region
```

will error with a message that Nautobot's `dcim.Region` Model has been
replaced with `dcim.Location`.

```shell
pylint nautobot_app/ \
  --rcfile=pyproject.toml \
  --disable=all \
  --enable="nautobot-replaced-models"

************* Module nautobot_app.models
nautobot_app/models.py:1:0: E4211: Imports a model that has been replaced
(dcim.Region -> dcim.Location). (nb-replaced-region)

... output trimmed ...
```

## nb-replaced-site

Looks for imports of `dcim.Site` Model class to notify that this Model has
been replaced by the `dcim.Location` Model. For example,

```python
from nautobot.dcim.models import Site
```

will error with a message that Nautobot's `dcim.Site` Model has been
replaced with `dcim.Location`.

```shell
pylint nautobot_app/ \
  --rcfile=pyproject.toml \
  --disable=all \
  --enable="nautobot-replaced-models"

************* Module nautobot_app.models
nautobot_app/models.py:1:0: E4211: Imports a model that has been replaced
(dcim.Site -> dcim.Location). (nb-replaced-site)

... output trimmed ...
```

## nb-replaced-aggregate

Looks for imports of `ipam.Aggregate` Model class to notify that this Model has
been replaced by the `ipam.Prefix` Model. For example,

```python
from nautobot.ipam.models import Aggregate
```

will error with a message that Nautobot's `ipam.Aggregate` Model has been
replaced with `ipam.Prefix`.

```shell
pylint nautobot_app/ \
  --rcfile=pyproject.toml \
  --disable=all \
  --enable="nautobot-replaced-models"

************* Module nautobot_app.models
nautobot_app/models.py:1:0: E4211: Imports a model that has been replaced
(ipam.Aggregate -> ipam.Prefix). (nb-replaced-aggregate)

... output trimmed ...
```

!!! note
    `nautobot-replaced-models` can be used to include all linters provided
    below.
