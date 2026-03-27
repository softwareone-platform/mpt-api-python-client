# Testing

This document provides a high-level overview of the testing strategy for
`mpt-api-python-client` and points to the detailed guides for each test type.

## Guides

- [Unit test guide](unit_tests.md) — structure, conventions, tooling, and examples.
- [E2E test guide](e2e_tests.md) — directory layout, execution instructions, and environment setup.

For a quick validation run: `make check && make test`.

## Coverage

Coverage is collected automatically via `pytest-cov` with the following defaults:

- Source: `mpt_api_client/`
- Reports: terminal (missing lines) + XML (`coverage.xml`)
- Branch coverage enabled
- `__init__.py` files excluded

Results are reported to SonarCloud via `sonar-project.properties`.

## Shared Standards

This repository follows the shared testing standard from
[mpt-extension-skills](https://github.com/softwareone-platform/mpt-extension-skills):

- `standards/testing-standard.md`

