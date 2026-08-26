# Using the Library

This document describes common use-cases and scenarios for this library.

## General Usage

<<<<<<< HEAD
<<<<<<< HEAD
This library provides Pylint rules to enforce best practices and known issues with Nautobot code, specifically used in Nautobot Apps and Nautobot Jobs. 

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

Test whether the new rules are enabled by running the following (this is just a subset of the available rules):

```
> poetry run pylint --list-msgs-enabled | grep nb-
  nb-replaced-device-role (E4211)
  nb-replaced-rack-role (E4212)
  nb-replaced-ipam-role (E4213)
  nb-replaced-region (E4214)
  nb-replaced-site (E4215)
  nb-replaced-aggregate (E4216)
  nb-code-location-utilities (E4251)
```

You can now run `pylint` within your project as you normally would and the additional rules will be automatically checked.

## Viewing a Rule's Extended Description

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

## Uncertainty in Rules

Because Python is a dynamically-typed language, sometimes `pylint` can't infer with 100% certainty whether a given rule applies to a given line of code. In `pylint-nautobot` the convention is to name such rules as `nb-possible-*` to indicate that uncertainty, for example `nb-possible-readonly-cable-attribute` flags lines where there's assignment to a `cable` attribute that may be (but is not definitively) read-only in its implementation - contrast to `nb-readonly-cable-attribute`, which flags lines where `pylint` is _confident_ that the assignment is incorrect. When encountering a `nb-possible-` message from `pylint`, you'll have to evaluate whether the message is relevant (and should be fixed) or a false positive (in which case an inline `# pylint: disable=...` comment should be added).

## Supporting More Than One Nautobot Version

Rules are enabled based on the Nautobot version your project depends on (either explicitly in a `poetry.lock` file, or if not present, the version of Nautobot installed in the current Python environment), so if your project supports multiple versions, the rules may flag code that is valid for one version but invalid for another, even if you have written appropriate branching logic (with checks like `if nautobot.__version__.startswith("3."):`) to correctly handle these variants. In this case, once you have tested and verified that logic against the relevant Nautobot versions, you will likely need to write appropriate inline `# pylint: disable=...` comments to mark the different code paths as intentional.

### Code Deprecation Rules

In some cases, rules may issue a warning about code that is valid for all supported Nautobot version(s), but uses a deprecated pattern or API. For example, Nautobot 3.2 deprecated (but did not remove) certain patterns for interacting with Cable and cable-termination models that were the standard pattern in Nautobot 3.1 and earlier. The rules `nb-deprecated-cable-lookup` and `nb-deprecated-termination-a-b-lookup` issue a warning message if you are using these patterns in your code.

If your code needs to support Nautobot versions that differ in their preferred/deprecated approach (for example, cable logic targeting both versions 3.1 and 3.2) then using the deprecated pattern may be your best and simplest approach for now, rather than writing branching logic in your code to use different patterns for different Nautobot versions. In this case, unlike the previous section, your intent is likely to _replace_ the deprecated patterns in the future, just not yet, and so our recommendation is to disable such rules project-wide through your project configuration file, rather than inline with `# pylint: disable=...` comments:

```toml
[tool.pylint.messages_control]
disable = [
    # Re-enable once we drop support for Nautobot < 3.2, then migrate the reported call sites.
    "nb-deprecated-cable-lookup",
    "nb-deprecated-termination-a-b-lookup",
]
```

This way, when your app is updated to drop support for the older Nautobot version(s), you can just remove the relevant lines from the project configuration and immediately make it possible for `pylint` to flag all instances in your code that are still using the deprecated pattern(s) and can now be updated to use the new, preferred patterns.
=======
=======
>>>>>>> 053372b (Cookie updated targeting develop by NetworkToCode Cookie Drift Manager Tool)
## Use-cases and common workflows

## Screenshots

!!! warning "Developer Note - Remove Me!"
    Ideally captures every view exposed by the Library. Should include a relevant dataset.
<<<<<<< HEAD
>>>>>>> 3e7c854 (Cookie updated targeting develop by NetworkToCode Cookie Drift Manager Tool)
=======
>>>>>>> 053372b (Cookie updated targeting develop by NetworkToCode Cookie Drift Manager Tool)
