---
hide:
  - navigation
---

# Release Notes

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.1] - 2024-08-22

### Changed

- Remove `Tables` from fields `__all__` check (nautobot-use-fields-all) and add tests ([#83](https://github.com/nautobot/pylint-nautobot/pull/83))

### Housekeeping

- Removed upper bound on Python version ([#88](https://github.com/nautobot/pylint-nautobot/pull/88))
- Added upper bound on pylint version (due to #89) ([#88](https://github.com/nautobot/pylint-nautobot/pull/88))
- Switched tooling to `ruff` as per changes to the Nautobot App Template and removed `flake8`, `pydocstyle`, and `bandit` ([#88](https://github.com/nautobot/pylint-nautobot/pull/88))

## [0.3.0] - 2024-03-05

### Added

- Added `nb-use-fields-all` rule (#70)
- Added `nautobot-sub-class-name` rule (#74)

### Changed

- Improve incorrect base class checker (#72)
- Update CODEOWNERS (#68)

### Fixed

- Fix RTD docs build (#58)
- Fix `UIViewSet` sub class name (#76)
- Fix failing check when class doesNt# have a `Meta` class member (#77)

### Housekeeping

- Allow wider range of `importlib-resources` library (#78)

## [0.2.1] - 2023-09-01

### Changed

- Updates CODEOWNERS (#41)
- Improves rule help messages (#49)
- Fix scoping on string field blank/null checker (#49)
- Parametrize the base class checker by the Nautobot version (#44)

## [0.2.0] - 2023-06-28

### Added

- Model label construction checker (#28)
- Added `StatusModel` usage checker (#26)
- String field blank/null checker (#18)
- Incorrect base class checker (#9)

### Tests

- Changed test structure to better align with established pylint patterns (#28)

## [0.1.0] - 2023-05-31

Initial release with a few rules, tests, and documentation.
