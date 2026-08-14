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
