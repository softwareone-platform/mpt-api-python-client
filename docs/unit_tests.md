# Unit Tests

This guide covers the structure, tooling, and conventions for the unit test suite in
`mpt-api-python-client`.

## Directory Layout

```text
tests/
└── unit/
    ├── conftest.py      # Shared fixtures (http_client, async_http_client, DummyModel)
    ├── http/            # Transport, services, and mixins
    ├── models/          # Model, Collection, and Meta behavior
    ├── resources/       # Resource-domain services (accounts, catalog, …)
    ├── rql/             # RQL query builder
    ├── test_constants.py
    ├── test_exceptions.py
    └── test_mpt_client.py
```

## Running Tests

All commands run inside the Docker-based Makefile drivers.

```bash
make test                          # run the full unit suite
make test args="tests/unit/http"   # run a specific directory
make test args="-k test_create"    # run a specific test pattern
```

## Unit tests general rules

[Python Unit test general rules with examples](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/unittests.md#general-rules)

## Unit tests mocking

[Unit tests mocks wiht examples](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/unittests.md#mocking-rules)


