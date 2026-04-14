# Testing

Shared test rules live in
[standards/unittests.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/unittests.md).
This document covers repository-specific testing behavior only.

## Test Scope

The repository has two main test layers:

- [Unit tests](unit_tests.md) under [`tests/unit/`](../tests/unit) for transport, models,
  resources, and the RQL builder
- [End-to-end tests](e2e_tests.md) under [`tests/e2e/`](../tests/e2e) for live API coverage

`make test` runs the unit suite by default. E2E tests are opt-in and require live credentials.

## Commands

Run all test commands through Docker-based make targets:

```bash
make test
make test args="tests/unit/http"
make test args="tests/e2e"
make check
make check-all
```

Repository command mapping:

- `make test` runs `pytest` against `tests/unit` unless `args` overrides the path
- `make check` runs `ruff format --check`, `ruff check`, `flake8`, `mypy`, and `uv lock --check`
- `make check-all` runs both `check` and `test`

## Pytest And Coverage

- Source: `mpt_api_client/`
- Reports: terminal (missing lines) + XML (`coverage.xml`)
- Branch coverage enabled
- `__init__.py` files omitted from coverage reports

Results are reported to SonarCloud via `sonar-project.properties`.

Repository-specific pytest settings live in [`pyproject.toml`](../pyproject.toml), including:

- discovery under `tests`
- repository root on `pythonpath`
- import mode `importlib`
- async fixture loop scope and warning filters

## Repository Constraints

- E2E suites require configured MPT credentials and optional ReportPortal settings; see [e2e_tests.md](e2e_tests.md).
- Keep live API coverage in `tests/e2e/` separate from unit-only behavior in `tests/unit/`.
- When changing public client behavior, service mixins, resource modules, or query building, update the matching unit coverage.
