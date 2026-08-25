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
    ├── exchange/
    ├── helpdesk/
    ├── integration/
    ├── notifications/
    ├── program/
    ├── spotlight/
    └── streaming/
```

Most directories mirror an API domain. `streaming/` is the exception: it covers the
platform streaming read mode itself — the contract `stream()` implements — rather than
one domain, and uses whichever collection makes the case observable.

## Running Tests

```bash
make e2e                              # run the E2E suite
make e2e args="tests/e2e/catalog"     # run a subset of E2E tests
```

E2E tests need live API credentials and run against the real API, so they have their own
target: `make test` covers `tests/unit` only, and `make check-all` does not run them.

## Streaming Memory Coverage

`tests/e2e/streaming/test_sync_streaming.py` and its async twin assert the property
`stream()` exists for: memory stays bounded
however many records an export carries, the bound
[streaming.md](streaming.md#memory-characteristics) documents. It is the one suite whose
result depends on the size of the live dataset, so it carries requirements the rest of
`tests/e2e/` does not.

It streams operations-scoped `catalog.items`, which holds well over the 20,000 records the
coverage exports. The measurement is a `tracemalloc` allocation peak — Python allocations
rather than process resident size, so it does not move with allocator or kernel behaviour —
taken over three whole reads: a 2,000-record export, a 20,000-record export, and the same
20,000-record export buffered with `list()`. Ten times the records must not cost materially
more memory, and buffering the same export must cost far more, which is what shows the
measurement is sensitive enough to see buffering reintroduced.

Each case runs once per `StreamFormat`, because the property must hold for every wire format
and they reach it differently: `JSONL` reads one record per line, while `JSON` parses records
out of the `{$meta, data}` envelope incrementally — the easier one to regress, since the
obvious implementation deserializes the whole body first. The parametrisation enumerates the
enum, so a format added later is covered without editing the tests.

The comparison is against the peaks measured in the same run rather than an absolute byte
threshold, so it does not need recalibrating per environment. If the environment holds fewer
records than the coverage exports, the fixture fails with that count rather than passing on a
dataset too small to mean anything. `tests/e2e/streaming/memory_probe.py` documents the
protocol and the reasoning behind each constant.

## Streaming Integrity Coverage

`tests/e2e/streaming/test_sync_streaming_integrity.py` and its async twin cover the parts of
[the streaming contract](streaming.md#three-obligations-you-cannot-skip) that only a live
platform can demonstrate: a `$meta.deleted` deletion stub, that same stub withheld but still
counted under `skip_deleted`, the declared `MPT-Item-Count` reaching a progress receiver, and
an early close not reporting an incomplete export. Each case runs in both wire formats.

The stub cases provoke the contract's own race rather than simulating it: create a product,
open a stream ordered oldest-first so that row is emitted last, then hard-delete it once the
first record has arrived — the response headers are out by then, so the export's key snapshot
already contains it. This needs a collection large enough that the platform cannot pre-buffer
the body; on a small one the row streams back as a full record and no stub is produced. The
assertions therefore pin the stub itself, so a race that was lost fails rather than passing
on an absence.

Truncated transports and count mismatches are deliberately not covered here. Neither can be
requested from a live platform — one needs the API to abort mid-body, the other contradicts
the contract — so a test shaped like coverage for either would pass without exercising the
path. They belong at a layer that can control the server.

## Environment Variables

| Variable                   | Description                                        |
|----------------------------|----------------------------------------------------|
| `MPT_API_BASE_URL`         | MPT API base URL                                   |
| `MPT_API_TOKEN_VENDOR`     | Vendor API token                                   |
| `MPT_API_TOKEN_CLIENT`     | Client API token                                   |
| `MPT_API_TOKEN_OPERATIONS` | Operations API token                               |
| `MPT_API_TOKEN_EXTENSION`  | Extension API key (installation token / extension framework auth) |

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
