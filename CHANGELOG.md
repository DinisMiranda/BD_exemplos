# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Initial professional setup: tests, coverage, CI, docs, lint, SECURITY, CONTRIBUTING.

## [0.1.0] - 2025-02-24

### Added

- MySQL config loader from TOML (`bd_exemplos.config`).
- Shared MySQL connection helper (`bd_exemplos.db`).
- Shop seed script: suppliers, products, clients, orders, order lines (`seed_loja`).
- Library seed script: authors, books, readers, loans (`seed_biblioteca`).
- Unit tests and coverage (pytest, pytest-cov).
- GitHub Actions workflow for tests and coverage.
- Dependabot, CODEOWNERS, documentation (Google-style docstrings).

[Unreleased]: https://github.com/YOUR_ORG/BD_exemplos/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/YOUR_ORG/BD_exemplos/releases/tag/v0.1.0
