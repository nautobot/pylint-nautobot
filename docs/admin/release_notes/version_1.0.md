
## [v1.1.0 (2026-08-18)](https://github.com/nautobot/pylint-nautobot/releases/tag/v1.1.0)

### Added

- [#136](https://github.com/nautobot/pylint-nautobot/issues/136) - Added `django.test.TransactionTestCase` to the incorrect base class checker.
- [#141](https://github.com/nautobot/pylint-nautobot/issues/141) - Added checks for code affected by Nautobot 3.2+ changes to cable data models.

### Changed

- [#144](https://github.com/nautobot/pylint-nautobot/issues/144) - Changed nautobot min version check to not load on startup.

### Documentation

- [#141](https://github.com/nautobot/pylint-nautobot/issues/141) - Removed leftover incorrect references to `supported_nautobot_versions` configuration key.

### Housekeeping

- [#138](https://github.com/nautobot/pylint-nautobot/issues/138) - Added Python 3.14 support.
- Rebaked from the cookie `main`.

# v1.0 Release Notes

This document describes all new features and changes in the release `1.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Updated pylint from 3.x to 4.x.

## [v1.0.0 (2026-01-14)](https://github.com/nautobot/pylint-nautobot/releases/tag/v1.0.0)

### Breaking Changes

- [#133](https://github.com/nautobot/pylint-nautobot/issues/133) - Updated pylint from 3.x to 4.x.

