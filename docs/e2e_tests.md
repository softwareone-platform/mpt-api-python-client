# End-to-End Tests

End-to-end tests exercise the running MPT API and cover the full request/response lifecycle.
They live under `tests/e2e/` and rely on live credentials and configurable endpoints.

## Directory Layout

```text
tests/
└── e2e/
    ├── conftest.py      # E2E fixtures (mpt_vendor, mpt_client, mpt_operations)
    ├── accounts/
    ├── audit/
    ├── billing/
    ├── catalog/
    ├── commerce/
    ├── helpdesk/
    └── notifications/
```

## Running Tests

```bash
make test args="tests/e2e"    # run the E2E suite
make test args="tests/e2e/catalog"    # run a subset of E2E tests
```

E2E suites use `pytest` markers and live API credentials, so they run outside the default
`make test` invocation.

## Environment Variables

| Variable                   | Description          |
|----------------------------|----------------------|
| `MPT_API_BASE_URL`         | MPT API base URL     |
| `MPT_API_TOKEN_VENDOR`     | Vendor API token     |
| `MPT_API_TOKEN_CLIENT`     | Client API token     |
| `MPT_API_TOKEN_OPERATIONS` | Operations API token |

### Optional ReportPortal Integration

| Variable      | Description               |
|---------------|---------------------------|
| `RP_API_KEY`  | ReportPortal API key      |
| `RP_ENDPOINT` | ReportPortal endpoint URL |
| `RP_LAUNCH`   | ReportPortal launch name  |

## Configuration

E2E test configuration lives in `e2e_config.test.json`.
Set the required environment variables before invoking the suite to avoid credential
validation failures.

Test results are published to [Report Portal](https://report-portal.s1.team/).


