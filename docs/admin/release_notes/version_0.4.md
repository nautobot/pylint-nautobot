## [v0.4.3 (2025-10-28)](https://github.com/nautobot/pylint-nautobot/releases/tag/v0.4.3)

### Added

- [#126](https://github.com/nautobot/pylint-nautobot/issues/126) - Added rule E4293 (nb-deprecated-class) to identify Python classes that are using base classes removed in Nautobot v3.0.

## [0.4.2] - 2025-07-09

### Added

- Added check to ensure filter field name does not have a double underscore [#120](https://github.com/nautobot/pylint-nautobot/pull/120)

### Fixed

- Fixed find_model_name to check for the model attribute first in the Meta class [#122](https://github.com/nautobot/pylint-nautobot/pull/122)

## [0.4.1] - 2025-06-03

### Changed

- Allow Nautobot prerelease versions in `is_version_compatible` [#114](https://github.com/nautobot/pylint-nautobot/pull/114)

## [0.4.0] - 2025-05-22

### Added

- Added support for Pylint 3.x [#108](https://github.com/nautobot/pylint-nautobot/pull/108)
- Added support for Python 3.12 [#108](https://github.com/nautobot/pylint-nautobot/pull/108)
- Added support for Python 3.13 [#111](https://github.com/nautobot/pylint-nautobot/pull/111)
- Added support for Nautobot 3.x [#111](https://github.com/nautobot/pylint-nautobot/pull/111)
- Implement a checker to validate that q uses SearchFilter [#107](https://github.com/nautobot/pylint-nautobot/pull/107)
- Add information on writing Custom Pylint Checkers [#105](https://github.com/nautobot/pylint-nautobot/pull/105)

### Changed

- Update developer docs [#96](https://github.com/nautobot/pylint-nautobot/pull/96)

### Fixed

- Updated tests to support pylint updates [#108](https://github.com/nautobot/pylint-nautobot/pull/108)

### Housekeeping

- Dropped support for Python 3.8 [#108](https://github.com/nautobot/pylint-nautobot/pull/108)
- Removed mkdocstrings [#108](https://github.com/nautobot/pylint-nautobot/pull/108)
- Pinned CI poetry version to use 1.8.5 [#107](https://github.com/nautobot/pylint-nautobot/pull/107)
