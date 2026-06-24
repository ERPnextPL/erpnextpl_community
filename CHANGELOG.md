# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2026-06-24

### Added
- **Polish banks list** – new idempotent patch `create_polish_banks.py` that
  creates the 15 largest Polish banks (name, website, SWIFT/BIC code). Existing
  `Bank` records are never overwritten.
- **Salary slip print format** – new `Pasek Wynagrodzenia - Timesheet` print
  format for `Salary Slip` (Jinja, default language `pl`).

### Changed
- Updated Polish translations in `translations/pl.csv` (payment entry settings,
  account balances and more).
- Unified internal module name: package path renamed from `erpnextpl/` to
  `erpnextpl_community/`; `modules.txt` updated to `ERPNextPL Community`; patch
  paths in `patches.txt` and references in `README.md` updated accordingly.

### Removed
- Dropped the unused `remove_pro_artifacts.py` patch (a Pro-variant artifact,
  out of scope for the Community edition).

### Migration notes
- Run `bench migrate` after upgrading to apply the new patches.
- No breaking changes for user data — patches are idempotent and do not
  overwrite existing records.

## [1.0.1]
- Path and CI fixes, README updates.

## [1.0.0]
- Initial public release.
