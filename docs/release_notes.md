---
hide:
  - navigation
---

# Release Notes

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-04

### Added

- Added support for Pylint 3.x [#108](https://github.com/nautobot/pylint-nautobot/pull/108)
- Added support for Python 3.12 [#108](https://github.com/nautobot/pylint-nautobot/pull/108)
- Added support for Python 3.13 [#111](https://github.com/nautobot/pylint-nautobot/pull/111)
- Added support for Nautobot 3.x [#111](https://github.com/nautobot/pylint-nautobot/pull/111)
- Implement a checker to validate that q uses SearchFilter [#107](https://github.com/nautobot/pylint-nautobot/pull/107)
- Add information on writing Custom Pylint Checkers [#105](https://github.com/nautobot/pylint-nautobot/pull/105)

## Changed

- Update developer docs [#96](https://github.com/nautobot/pylint-nautobot/pull/96)

### Fixed

- Updated tests to support pylint updates [#108](https://github.com/nautobot/pylint-nautobot/pull/108)

### Housekeeping

- Dropped support for Python 3.8 [#108](https://github.com/nautobot/pylint-nautobot/pull/108)
- Removed mkdocstrings [#108](https://github.com/nautobot/pylint-nautobot/pull/108)
- Pinned CI poetry version to use 1.8.5 [#107](https://github.com/nautobot/pylint-nautobot/pull/107)

## [0.3.1] - 2024-08-22

### Changed

- Remove `Tables` from fields `__all__` check (nautobot-use-fields-all) and add tests ([#83](https://github.com/nautobot/pylint-nautobot/pull/83))

### Housekeeping

- Removed upper bound on Python version ([#88](https://github.com/nautobot/pylint-nautobot/pull/88))
- Added upper bound on pylint version (due to #89) ([#88](https://github.com/nautobot/pylint-nautobot/pull/88))
- Switched tooling to `ruff` as per changes to the Nautobot App Template and removed `flake8`, `pydocstyle`, and `bandit` ([#88](https://github.com/nautobot/pylint-nautobot/pull/88))

## [0.3.0] - 2024-03-05

### Added

- Added `nb-use-fields-all` rule [#70](https://github.com/nautobot/pylint-nautobot/pull/70)
- Added `nautobot-sub-class-name` rule [#74](https://github.com/nautobot/pylint-nautobot/pull/74)

### Changed

- Improve incorrect base class checker [#72](https://github.com/nautobot/pylint-nautobot/pull/72)
- Update CODEOWNERS [#68](https://github.com/nautobot/pylint-nautobot/pull/68)

### Fixed

- Fix RTD docs build [#58](https://github.com/nautobot/pylint-nautobot/pull/58)
- Fix `UIViewSet` sub class name [#76](https://github.com/nautobot/pylint-nautobot/pull/76)
- Fix failing check when class doesNt# have a `Meta` class member [#77](https://github.com/nautobot/pylint-nautobot/pull/77)

### Housekeeping

- Allow wider range of `importlib-resources` library [#78](https://github.com/nautobot/pylint-nautobot/pull/78)

## [0.2.1] - 2023-09-01

### Changed

- Updates CODEOWNERS [#41](https://github.com/nautobot/pylint-nautobot/pull/41)
- Improves rule help messages [#49](https://github.com/nautobot/pylint-nautobot/pull/49)
- Fix scoping on string field blank/null checker [#49](https://github.com/nautobot/pylint-nautobot/pull/49)
- Parametrize the base class checker by the Nautobot version [#44](https://github.com/nautobot/pylint-nautobot/pull/44)

## [0.2.0] - 2023-06-28

### Added

- Model label construction checker [#28](https://github.com/nautobot/pylint-nautobot/pull/28)
- Added `StatusModel` usage checker [#26](https://github.com/nautobot/pylint-nautobot/pull/26)
- String field blank/null checker [#18](https://github.com/nautobot/pylint-nautobot/pull/18)
- Incorrect base class checker [#9](https://github.com/nautobot/pylint-nautobot/pull/9)

### Tests

- Changed test structure to better align with established pylint patterns [#28](https://github.com/nautobot/pylint-nautobot/pull/28)

## [0.1.0] - 2023-05-31

Initial release with a few rules, tests, and documentation.
