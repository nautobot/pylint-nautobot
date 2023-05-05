# Custom Pylint Rules for Nautobot

## Testing and developing

Clone a repo:

```
vagrant@ants:~
> git clone https://github.com/nautobot/nautobot-plugin-golden-config
Cloning into 'nautobot-plugin-golden-config'...
remote: Enumerating objects: 2221, done.
remote: Counting objects: 100% (250/250), done.
remote: Compressing objects: 100% (152/152), done.
remote: Total 2221 (delta 134), reused 183 (delta 91), pack-reused 1971
Receiving objects: 100% (2221/2221), 4.72 MiB | 19.19 MiB/s, done.
Resolving deltas: 100% (1356/1356), done.
```

Install `pylint-nautobot` in editable mode from your cloned repo:

```
vagrant@ants:~/nautobot-plugin-golden-config (develop *=)
> poetry add --editable /path/to/pylint-nautobot/

Updating dependencies
Resolving dependencies... (0.8s)

Writing lock file
```

Enable the `pylint-nautobot` plugin in `pyproject.toml`:

```
[tool.pylint.master]
load-plugins="pylint_django, pylint_nautobot"
```

Test the new rules are enabled:

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

## Testing and developing - with `pylint 2.17` and `python 3.7.2`

Clone a repo:

```
vagrant@ants:~
> git clone https://github.com/nautobot/nautobot-plugin-golden-config
Cloning into 'nautobot-plugin-golden-config'...
remote: Enumerating objects: 2221, done.
remote: Counting objects: 100% (250/250), done.
remote: Compressing objects: 100% (152/152), done.
remote: Total 2221 (delta 134), reused 183 (delta 91), pack-reused 1971
Receiving objects: 100% (2221/2221), 4.72 MiB | 19.19 MiB/s, done.
Resolving deltas: 100% (1356/1356), done.
```

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

Install `pylint-nautobot` in editable mode from your cloned repo:

```
vagrant@ants:~/nautobot-plugin-golden-config (develop *=)
> poetry add --editable /path/to/pylint-nautobot/

Updating dependencies
Resolving dependencies... (3.2s)

Writing lock file

Package operations: 2 installs, 3 updates, 0 removals

  • Updating astroid (2.11.7 -> 2.15.2)
  • Updating text-unidecode (1.3 /home/vagrant/.cache/pypoetry/artifacts/34/ff/90/dfdc177dbd51133d449192d5f6c8bd34ced8d4c3ce8f648a5cbcacd517/text_unidecode-1.3-py2.py3-none-any.whl -> 1.3)
  • Installing tomlkit (0.11.7)
  • Updating pylint (2.13.9 -> 2.17.2)
  • Installing pylint-nautobot (0.1.0 /vagrant)
```

Enable the `pylint-nautobot` plugin in `pyproject.toml`:

```
[tool.pylint.master]
load-plugins="pylint_django, pylint_nautobot"
```

Test the new rules are enabled:

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
************* Module /home/vagrant/nautobot-plugin-golden-config/pyproject.toml
pyproject.toml:1:0: R0022: Useless option value for '--disable', 'bad-continuation' was removed from pylint, see https://github.com/PyCQA/pylint/pull/3571. (useless-option-value)
************* Module nautobot_golden_config.forms
nautobot_golden_config/forms.py:1:0: E5110: Django was not configured. For more information run pylint --load-plugins=pylint_django --help-msg=django-not-configured (django-not-configured)
nautobot_golden_config/forms.py:7:0: E4214: Imports a model that has been replaced (dcim.Region -> dcim.Location). (nb-replaced-region)
nautobot_golden_config/forms.py:7:0: E4215: Imports a model that has been replaced (dcim.Site -> dcim.Location). (nb-replaced-site)
nautobot_golden_config/forms.py:7:0: E4211: Imports a model that has been replaced (dcim.DeviceRole -> extras.Role). (nb-replaced-device-role)
nautobot_golden_config/forms.py:10:0: E4251: Import location has changed (nautobot.utilities.forms -> nautobot.core.forms). (nb-code-location-utilities)

------------------------------------------------------------------
Your code has been rated at 7.73/10 (previous run: 7.73/10, +0.00)
```

Enjoy the new rules (codes starting with `E42`) and ignore all the new stuff pylint 2.17 complains about!
