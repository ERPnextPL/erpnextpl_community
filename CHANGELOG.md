# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Polish tax identifiers on Supplier and Company** – the `Polish Tax Identifiers`
  section previously available only on `Customer` is now also added to `Supplier`
  and `Company` (#4). On `Customer` and `Supplier` it holds `REGON`, `KRS`, `PESEL`
  and `VAT Tax Status`: REGON/KRS are shown for companies and PESEL for individuals.
  On `Company` it holds `REGON`, `KRS` and `VAT Tax Status` (no PESEL; the company
  is identified by NIP).
- **Setup on fresh installs** – new `after_install` hook creates the Custom Fields,
  print formats, email templates, notifications (disabled) and Polish banks, and
  enables the Polish language. Previously `bench install-app` only marked the
  patches as executed, so fresh sites got none of these.

### Changed
- The `Polish Tax Identifiers` section on `Customer` and `Supplier` is now at the
  top of the Settings tab instead of after `tax_withholding_category`.
- CI now tests against Frappe / ERPNext `version-16` (Python 3.14, Node 24,
  MariaDB 11.8) instead of `version-15`.

### Migration notes
- New idempotent patch `add_polish_tax_fields_to_supplier_and_company` adds the
  fields on existing sites during `bench migrate`. Custom Fields that already exist
  (e.g. added manually) are not modified.
- New patch `move_polish_tax_section_to_settings_tab` moves the existing section on
  `Customer` and `Supplier` to the Settings tab, only if it is still in its previous
  default place.

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
