# Development

This section of the docs explains how to to development in this repository.

## Version specifiers

Every check should have a class variable called `version_specifier` of type `packaging.specifiers.SpecifierSet` that specifies to which versions of Nautobot a check applies:

The following example is a checker that applies to all projects targeting any Nautobot 2.x.y version:

```python
from packaging.specifiers import SpecifierSet
from pylint.checkers import BaseChecker

class NautobotSpecificExampleChecker(BaseChecker):
    version_specifier = SpecifierSet(">=2,<3")

    ...
```

!!! note
    For a detailed overview of how you can specify versions take a look at [PEP440](https://peps.python.org/pep-0440/#version-specifiers). However, in general you should strive for as simple as possible version specifiers.

## Testing Rules in a Specific Nautobot App

Clone a repository containing a specific Nautobot App:

```
vagrant@ants:~
> git clone https://github.com/nautobot/nautobot-plugin-golden-config
```

Install `pylint-nautobot` in editable mode from your cloned repo:

```
vagrant@ants:~/nautobot-plugin-golden-config (develop *=)
> poetry add --editable /path/to/pylint-nautobot/
```

Enable and configure the `pylint-nautobot` plugin in the target App's `pyproject.toml`:

```
[tool.pylint.master]
load-plugins="pylint_django, pylint_nautobot"

...

[tool.pylint-nautobot]
supported_nautobot_versions = [
    "1",
    "2"
]
```

Test whether the new rules are enabled:

```
vagrant@ants:~/nautobot-plugin-golden-config (develop *=)
> poetry run pylint --list-msgs-enabled | grep E42
  nb-replaced-device-role (E4211)
  nb-replaced-rack-role (E4212)
  nb-replaced-ipam-role (E4213)
  nb-replaced-region (E4214)
  nb-replaced-site (E4215)
  nb-replaced-aggregate (E4216)
  nb-code-location-utilities (E4251)
```

Run `pylint`:

```
vagrant@ants:~/nautobot-plugin-golden-config (develop *=)
> poetry run pylint nautobot_golden_config/forms.py
************* Module nautobot_golden_config.forms
nautobot_golden_config/forms.py:1:0: E5110: Django was not configured. For more information run pylint --load-plugins=pylint_django --help-msg=django-not-configured (django-not-configured)
nautobot_golden_config/forms.py:7:0: E4214: Imports a model that has been replaced (dcim.Region -> dcim.Location). (nb-replaced-region)
nautobot_golden_config/forms.py:7:0: E4215: Imports a model that has been replaced (dcim.Site -> dcim.Location). (nb-replaced-site)
nautobot_golden_config/forms.py:7:0: E4211: Imports a model that has been replaced (dcim.DeviceRole -> extras.Role). (nb-replaced-device-role)
nautobot_golden_config/forms.py:10:0: E4251: Import location has changed (nautobot.utilities.forms -> nautobot.core.forms). (nb-code-location-utilities)

-----------------------------------
Your code has been rated at 7.73/10
```

TODO - run it properly through invoke instead to avoid other detections.

## Using `pylint 2.17`

Update the minimum python version to `3.7.2` to allow the usage of the latest stable `pylint 2.17`:

```
vagrant@ants:~/nautobot-plugin-golden-config (develop *=)
> sed -i 's/python = "^3.7"/python = "^3.7.2"/' pyproject.toml

vagrant@ants:~/nautobot-plugin-golden-config (develop *=)
> git diff pyproject.toml
diff --git a/pyproject.toml b/pyproject.toml
index 3f6d7c9..7b82515 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -29,7 +29,7 @@ packages = [
 ]

 [tool.poetry.dependencies]
-python = "^3.7"
+python = "^3.7.2"
 deepdiff = ">=5.5.0,>=6.2.0"
 django-pivot = "^1.8.1"
 matplotlib = "^3.3.2"
```
