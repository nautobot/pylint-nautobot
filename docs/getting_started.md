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

### Supporting more than one Nautobot version

Rules are enabled based on the Nautobot version your project resolves to, so a rule can fire on code that is
deliberately written to work across several Nautobot versions. This happens when a newer Nautobot release
deprecates a pattern but the replacement does not exist in the older releases you still support — the deprecated
spelling is then the only one available to you, and the rule has no better suggestion to offer.

The Nautobot 3.2 Cable data model rules are the current example. `nb-deprecated-cable-lookup` and
`nb-deprecated-termination-a-b-lookup` flag lookups that Nautobot 3.2 still honors but reports a
`DeprecationWarning` for; their replacements (`cable_termination__...` and `terminations__...`) were introduced in
3.2, so an App that also supports 3.1 cannot use them.

These rules are still enabled by default. If they do not apply to your project yet, disable them explicitly and
record why, so the suppression can be removed once you raise your minimum Nautobot version:

```toml
[tool.pylint.messages_control]
disable = [
    # Re-enable once we drop support for Nautobot < 3.2, then migrate the reported call sites.
    "nb-deprecated-cable-lookup",
    "nb-deprecated-termination-a-b-lookup",
]
```

Note that this applies only to the `nb-deprecated-*` rules. The rules reporting code that fails outright on
Nautobot 3.2 (`nb-removed-cable-field`, `nb-removed-termination-a-b-field`, `nb-readonly-cable-attribute`, and
friends) are actionable on every supported version and should not be disabled.

## Authors and Maintainers

- [Cristian Sirbu](https://github.com/cmsirbu)
- [Leo Kirchner](https://github.com/Kircheneer)
- Nautobot Core Team (TBD)

## Frequently Asked Questions

Please ask us questions! You can swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#nautobot`), sign up [here](http://slack.networktocode.com/) if you don't have an account.
