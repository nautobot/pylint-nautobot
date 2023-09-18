---
hide:
  - navigation
---

# Getting Started

## Overview

This project packages together custom rules for the `pylint` Python linter. These rules are meant to aid developers within the Nautobot ecosystem (i.e. core application, plugins/apps, jobs etc.) by highlighting good practices, unwanted coding patterns, or outright errors when migrating code between major releases of Nautobot (which have backwards incompatible changes).

### Audience (User Personas) - Who should use this project?

Nautobot ecosystem developers and maintainers can add these rules to their development environment and CI pipelines.

## Usage in an Existing Project

`pylint-nautobot` is published on PyPI and can be installed with any of the usual Python packaging tools (e.g. `pip`, `poetry` etc.).

!!! warning
    Currently we only support providing plugin configuration via `pyproject.toml`.

To add `pylint-nautobot` to an existing project, first add it as a "dev" dependency via `poetry`:

```
> poetry add pylint-nautobot --group dev
```

`pylint-nautobot` is a `pylint` plugin, so you need to enable in its respective `pyproject.toml` section (add it to the comma-separated list if there's already others in place):

```
[tool.pylint.master]
load-plugins="pylint_nautobot"
```

Then, add a configuration section for `pylint-nautobot` itself, which dynamically enables or disables rules based on the target supported Nautobot version(s) for your code:

```
[tool.pylint-nautobot]
supported_nautobot_versions = [
    "1",
    "2"
]
```

!!! note
    Here, you are telling `pylint` that you want all rules for Nautobot versions 1.x.y and 2.x.y to be checked.

Test whether the new rules are enabled by running the following (this is just a subset of the available rules):

```
> poetry run pylint --list-msgs-enabled | grep E42
  nb-replaced-device-role (E4211)
  nb-replaced-rack-role (E4212)
  nb-replaced-ipam-role (E4213)
  nb-replaced-region (E4214)
  nb-replaced-site (E4215)
  nb-replaced-aggregate (E4216)
  nb-code-location-utilities (E4251)
```

You can now run `pylint` within your project as you normally would and the additional rules will be automatically checked.

### Viewing a rule's extended description

Sometimes the short name of the rule displayed in the output of `pylint` will not be enough to understand the problem:

```
nautobot_golden_config/models.py:216:4: E4261: Uses bad parameter combination for TextField/CharField. (nb-string-field-blank-null)
```

All rules also have additional information that can be viewed with the `--help-msg=rule-id` command line parameter:

```
> poetry run pylint --help-msg=E4261
:nb-string-field-blank-null (E4261): *Uses bad parameter combination for TextField/CharField.*
  Don't use blank=true and null=true on TextField or CharField. It avoids
  confusion between a value of None and a value of "" potentially having
  different meanings. This message belongs to the nautobot-string-field-blank-
  null checker.
```

## Authors and Maintainers

- [Cristian Sirbu](https://github.com/cmsirbu)
- [Leo Kirchner](https://github.com/Kircheneer)
- Nautobot Core Team (TBD)

## Frequently Asked Questions

Please ask us questions! You can swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#nautobot`), sign up [here](http://slack.networktocode.com/) if you don't have an account.
