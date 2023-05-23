---
hide:
  - navigation
---
# Development

## Contributing

The project is packaged with a light development environment using `invoke` tasks to help with the local development of the project and to run tests.

The project is following Network to Code software development guidelines and is leveraging the following:

- Python linting and formatting: `black`, `pylint`, `bandit`, `flake8`, and `pydocstyle`.
- YAML linting is done with `yamllint`.
- Python unit tests to ensure the rules are working properly.

You can find all the Markdown source for the project documentation under the [`docs`](https://github.com/nautobot/pylint-nautobot/tree/main/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient: clone the repository and edit away.

If you need to view the fully-generated documentation site, you can build it with [MkDocs](https://www.mkdocs.org/) by running `invoke docs` in your local development environment. As your changes to the documentation files are saved, they will be automatically rebuilt and any pages currently being viewed will be reloaded in your browser.

## Extending the Linting Rules

Extending the rules is welcome, however it is best to open an issue first, to ensure that a PR would be accepted and makes sense in terms of coverage and design.

## Adding New Rules

To add new rules, either add them to an existing category/checker (if it makes sense) or create a new one. Each checker is a class (e.g. `class NautobotCodeLocationChangesChecker(BaseChecker)`) which implements one or more `pylint` rules.

### Version Specifiers

Every check should have a class variable called `version_specifier` which is a string that follows the `packaging.specifiers.SpecifierSet` syntax. It is used as a filter for which versions of Nautobot a check applies to.

The following example is a checker that applies to all projects targeting any Nautobot `2.x.y` version:

```python
from pylint.checkers import BaseChecker

class NautobotSpecificExampleChecker(BaseChecker):
    version_specifier = ">=2,<3"
    ...
```

!!! note
    For a detailed overview of how you can specify versions take a look at [PEP440](https://peps.python.org/pep-0440/#version-specifiers). However, in general you should strive for as simple as possible version specifiers.

### Testing Rules in a Specific Nautobot App

To test your new rules on another Nautobot project while developing, you can add your local `pylint-nautobot` environment in editable mode to it.

First, clone a repository containing a specific Nautobot App:

```
> git clone https://github.com/nautobot/nautobot-plugin-golden-config
```

Install `pylint-nautobot` in editable mode from your cloned repo:

```
> cd nautobot-plugin-golden-config
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

!!! note
    Here, you are telling `pylint` that you want all rules for Nautobot versions 1.x.y and 2.x.y to be checked.

Test whether the new rules are enabled, replacing the message codes with your own, by running the following in the `nautobot-plugin-golden-config` folder:

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

While developing, you'll want to scope the linting only to your current set of rules - for example, here we're only testing for the `nautobot-code-location-changes` group of rules:

```
> poetry run pylint nautobot_golden_config --disable=all --enable=nautobot-code-location-changes

************* Module nautobot_golden_config.navigation
nautobot_golden_config/navigation.py:4:0: E4251: Import location has changed (nautobot.utilities.choices -> nautobot.core.choices). (nb-code-location-changed)
************* Module nautobot_golden_config.forms
nautobot_golden_config/forms.py:10:0: E4251: Import location has changed (nautobot.utilities.forms -> nautobot.core.forms). (nb-code-location-changed)
nautobot_golden_config/forms.py:12:0: E4252: Import location has changed for TreeModelSerializerMixin (nautobot.core.api.utils -> nautobot.core.api.serializers). (nb-code-location-changed-object)
nautobot_golden_config/forms.py:13:0: E4252: Import location has changed for deepmerge (nautobot.utilities.utils -> nautobot.core.utils.data). (nb-code-location-changed-object)
************* Module nautobot_golden_config.tables
nautobot_golden_config/tables.py:9:0: E4251: Import location has changed (nautobot.utilities.tables -> nautobot.core.tables). (nb-code-location-changed)

... output trimmed ...
```

Should you want to perform the full `pylint` suite of tests, follow the project's development setup (for Nautobot Apps typically `invoke pylint`).
