# Streaming

This guide is for developers who need to read a large result set out of the MPT API in one
pass. It covers when to stream instead of paging, what the platform guarantees about a
stream, and the obligations a consumer must meet to read one correctly.

For installation, client construction, and the general sync and async patterns, see
[usage.md](usage.md). For where the streaming mixins and exceptions sit in the codebase, see
[architecture.md](architecture.md).

## `stream()` Versus `iterate()`

Both read a whole collection. They differ in how the platform produces the result and in
what the client can guarantee about it.

| | `iterate()` | `stream()` |
|---|---|---|
| Requests | One request per page | One request for the whole export |
| Read mode | Regular paged read | Streaming mode, opted into with `MPT-Streaming: true` |
| Membership | Re-evaluated on every page | Fixed once, when the stream opens |
| Response format | `application/json` page envelope | either wire format, chosen per request |
| Completeness | Not verifiable | Verified against `MPT-Item-Count` |
| Deleted members | Absent from later pages | Emitted as a `DeletionStub` |
| Recovery from failure | Re-fetch the failed page | Restart the whole export |
| Peak memory | One page | One record |

Use `iterate()` when you want the collection as it is right now and you will consume all of
it promptly: it is the plain paged read, and a failure costs one page. Use it also for
endpoints that do not stream, and as the fallback when streaming is refused.

Use `stream()` when you need a consistent export rather than a live read — a nightly sync, a
reconciliation job, a bulk load into another system. Streaming asks the platform for a
point-in-time export, so the result set does not shift underneath you while you read it, and
the client can tell you whether you received all of it.

`stream()` is not a faster `iterate()` for small reads. It costs the platform a key scan
before the first byte and it costs you the three obligations below. For a few hundred
records, page.

### Every Collection Service Streams

`CollectionMixin` and `AsyncCollectionMixin` inherit `StreamingMixin` and
`AsyncStreamingMixin`, so `stream()` is available on every collection service without
per-service wiring:

```python
from mpt_api_client import BearerTokenAuthentication, MPTClient, RQLQuery

client = MPTClient.from_config(
    authentication=BearerTokenAuthentication("<token>"),
    base_url="https://api.s1.show/public",
)

for order in client.commerce.orders.filter(RQLQuery(status="Processing")).stream():
    print(order.id)
```

Streaming mode is a property of the request, not of the service. The route is the ordinary
collection route, so `filter()`, `order_by()` and `select()` chain before `stream()` exactly
as they do before `iterate()`; the client turns the read into a stream by sending the
`MPT-Streaming` header.

You can assume a standard collection endpoint streams: the platform's shared framework
provides streaming mode on its standard read controller, and every list endpoint is expected
to support it. Two cases are the exception rather than the rule. A hand-written list action —
one with a mandatory scoping filter, or one that already assigns a media type its own meaning
— opts in explicitly. And an endpoint that has not picked up the rollout answers `501`.

That `501` is an ordinary, expected answer rather than a fault, surfaced as
`MPTStreamingNotSupportedError`. Handle it by falling back to `iterate()`, not by checking
endpoints up front:

```python
from mpt_api_client.exceptions import MPTStreamingNotSupportedError

try:
    records = list(client.commerce.orders.stream())
except MPTStreamingNotSupportedError:
    records = list(client.commerce.orders.iterate())
```

### Do Not Confuse `stream()` With `stream_jsonl()`

The two methods look alike and mean different things.

| | `stream()` | `stream_jsonl()` |
|---|---|---|
| Contract | The platform streaming read mode | An endpoint's own JSONL download |
| `MPT-Streaming` header | Sent, and the response must confirm it | Not sent |
| Completeness check | Yes | No |
| Yields | Models or `DeletionStub` objects | Models only |
| Availability | Every collection service | Composed explicitly, today only by billing statement charges |

A service can carry both, and billing statement charges does: `stream_jsonl()` is its JSONL
download, while `stream()` is the streaming-mode read it inherits with every other
collection service. Reach for `stream_jsonl()` only when you specifically want that
endpoint's JSONL contract; for everything else `stream()` is the streaming read.

## Memory Characteristics

`stream()` holds one record at a time. The response body is parsed as it arrives and each
record is deserialized, yielded, and dropped, so peak memory is set by the largest single
record rather than by the size of the export. A ten-million-record stream costs the same as a
ten-record one. This holds in both wire formats — the envelope is tokenized incrementally
rather than buffered.

The buffering paths, for contrast:

- `iterate()` holds one page. It buffers each page response in full, deserializes it into a
  `ModelCollection`, and yields from that before fetching the next — so peak memory is
  `batch_size` records, 100 by default.
- `fetch_page()` and `fetch_one()` buffer a single response and return it whole.
- Any call that materializes the iterator — wrapping a stream in `list()`, a comprehension,
  a `sorted()` — buffers the entire result set and gives up the bound. That is a fine choice
  when you know the result is small, and it is the reason the short examples in this guide
  use it, but it is a decision to make on purpose rather than by accident.

The flat profile is a property of the loop, not of the method. Keep the per-record work
inside the `for` body — write, upsert, aggregate — and the whole export stays bounded.

## What A Stream Is

The platform builds an export in two phases. Phase one scans keys and fixes the membership
of the export; phase two reads the records for those keys in batches and writes them to the
response body.

Two consequences follow, and both are contract-conformant behaviour that will otherwise read
as a bug:

- **Membership is fixed when the stream opens.** Records created after that point are not in
  the export, and rows whose filter columns change after that point are not ejected from it.
  A stream is a point-in-time export, not a live paged read.
- **Record content is the committed state at batch read time**, so a record's contents can
  postdate the moment membership was fixed. There is no cross-record point-in-time
  consistency: record A can be newer than record B in the same export.

A record whose access is revoked mid-export still streams, because security-context filters
are applied when membership is fixed and are not re-applied per batch.

The longer an export runs over frequently written data, the wider the drift between
membership and content: expect more deletion stubs and more post-snapshot content on a long
export than on a short one.

## Choosing The Wire Format

Streaming mode and the wire format are two independent per-request choices. The
`MPT-Streaming` header selects streaming; `Accept` selects the encoding, and `stream()`
exposes it as `stream_format`:

| `stream_format` | `Accept` | Body |
|---|---|---|
| `StreamFormat.JSONL` (default) | `application/jsonl` | one record object per line, no envelope |
| `StreamFormat.JSON` | `application/json` | the standard `{$meta, data}` envelope, the same shape `iterate()` reads |

```python
from mpt_api_client.http.mixins import StreamFormat

for order in client.commerce.orders.stream(stream_format=StreamFormat.JSON):
    print(order.id)
```

A `StreamFormat` member or its `Accept` string is accepted; any other value raises
`ValueError` before the request is sent, rather than failing deep in header construction.

**Both formats are parsed as the body arrives**, so the memory bound described above holds
either way. In envelope format the JSON is tokenized incrementally: a record is deserialized
when its own closing brace arrives, not when the envelope completes.

Keep-alives differ in shape and are invisible either way. The line-delimited format emits
blank lines; the envelope format emits insignificant whitespace between tokens, consumed
while tokenizing. Neither reaches your loop, and neither counts as a record.

The total does not depend on the format: in both, a `progress` receiver gets the declared
`MPT-Item-Count` through `set_total_items`, exactly once, before the first record arrives,
so a progress report can render a percentage of a streamed export either way. The envelope
also carries `$meta.pagination.total` — contractually a mirror of the header, likewise the
capped `min(matches, N)` under a bounded `limit=N` — which the client does not re-report:
the header stays the single source of the receiver's total.

Pick the line-delimited format when you want the simplest thing to store or pipe: one record
per line survives `split`, `tail` and append-only files, where a single enclosing envelope
does not; pick the envelope when a consumer expects the standard `{$meta, data}` shape.

Everything else is format-independent: query state, `limit` and `offset`, deletion stubs, the
completeness check against `MPT-Item-Count`, the total reported to `progress`, and every
streaming error.

## Bounding An Export

`limit` selects between the whole snapshot and a bounded prefix of it:

| `limit` | Meaning |
|---|---|
| absent (default) | The full snapshot |
| `-1` | The same thing, stated explicitly |
| `N` | The first `N` records of the stream order |

Under a bounded `limit=N`, the count the response declares is the capped count,
`K = min(matches, N)` — not the uncapped number of matches. Both carriers agree:
`MPT-Item-Count` and, in the envelope format, `$meta.pagination.total`. The completeness check
compares against that capped value, so a bounded export verifies exactly like a full one.

```python
for order in client.commerce.orders.order_by("-audit.created.at").stream(limit=100_000):
    print(order.id)
```

`stream()` also accepts `offset`. Pagination inputs are sent exactly as given and are never
checked locally, because the server owns their validation: it currently rejects `offset` in
streaming mode with `400`, and support for it is scheduled. Passing through is correct either
way, so no client release is coupled to that change.

## Three Obligations You Cannot Skip

Streaming trades the safety of paging for a single-pass export. These three checks are what
you take on in exchange. Each prevents a failure that is silent without it.

### 1. Verify Completeness Against `MPT-Item-Count`

**Prevents:** processing a truncated export as if it were the whole result set.

Streaming mode commits the `MPT-Item-Count` response header together with the status: the
number of records the stream will carry. It is the contract's only completeness signal. The
envelope format's `$meta.pagination.total` carries the same number, but it precedes the data
and so cannot attest that the data arrived — it is a total to display, not a check to make.

`stream()` performs this check for you. It reads the declared count before yielding the first
record and compares it with the number of raw records consumed when the body ends —
consumed, not yielded, because `skip_deleted` filtering happens after this accounting:

- No usable count declared → `MPTStreamingItemCountMissingError`, raised before the body is
  read, so no partial data is consumed.
- Count mismatch on a fully consumed body → `MPTStreamingIncompleteError`.

A mismatch means the stream terminated gracefully but did not carry what it promised — an
intermediary swallowed part of the body, or the export was cut short. The records you
received are not a valid subset to keep, because you cannot tell which ones are missing.
Discard them and re-run the export.

Closing the iterator early does not raise. The check applies only to a stream consumed to
the end, so `break`-ing out of the loop on purpose is not reported as an incomplete export:

```python
for order in client.commerce.orders.stream():
    if order.id == "ORD-0000-0001":
        break  # deliberate early exit, no completeness check
```

The count does not survive persisting the payload. If you write the raw records to storage
and verify them later, store the expected count alongside them — once the response is gone,
the export's own completeness signal is gone with it.

The supported way to capture it is a `progress` receiver: `stream()` calls `set_total_items`
with the declared `MPT-Item-Count` before the first record, in both wire formats, so the
count is in hand before any record is written. `stream()` still yields records, not headers —
there is no need to drop to `client.http_client.stream(...)` just to read the header.

### 2. Check For A Deletion Stub Before Ingesting A Record

**Prevents:** overwriting a live stored record with nulls.

A member of the snapshot whose row is hard-deleted before phase two reaches it is still a
member of the export, so the platform emits a deletion stub in its place, marked with
`$meta.deleted` — the platform's metadata channel for the signal, and the name the API
contract uses for it:

```json
{"id": "ORD-1234-5678", "$meta": {"deleted": true}}
```

Only `id` is guaranteed on a stub. No other property of the deleted row is carried. A
**truthy** `deleted` marker is what identifies a stub; a record with no `$meta`, no `deleted`
key, or a falsy one is data. In practice the platform omits `$meta` entirely on a normal
record, so those cases are defensive rather than expected.

`stream()` yields these as `DeletionStub`, never as a model, so the object cannot be mistaken
for a record by code that expects one. Deserializing a stub as a model would produce an
instance whose every declared field is `None` — indistinguishable from a record whose values
really are unset — and a sync job writing that back would overwrite the stored record with
nulls. Branch on the type before ingesting the object; there is nothing else on a stub to
inspect:

```python
import uuid

from mpt_api_client.models import DeletionStub

# A fresh key per attempt. A retry opens a new snapshot, so it must never reuse one.
attempt_id = uuid.uuid4().hex

try:
    for result in client.commerce.orders.stream():
        if isinstance(result, DeletionStub):
            stage_delete(attempt_id, result.id)
        else:
            stage_upsert(attempt_id, result)

    # Reached only once stream() has verified the record count against MPT-Item-Count.
    promote(attempt_id)
except Exception:
    discard(attempt_id)
    raise
```

Note what the loop does *not* do: it stages rather than writes. `stream()` yields records
before it can verify the count, so applying each record as it arrives leaves partial local
state behind on a truncated export — the one thing
[Restart, Do Not Resume](#3-restart-do-not-resume) says must not survive a failed attempt.
Stage under an attempt key and promote after the loop, which is reached only on a verified
export.

Catch broadly rather than on `MPTStreamingError`, because not every failure that can strand a
staged attempt is one. A malformed body raises `json.JSONDecodeError`, and your own staging
code can fail too; either way promotion is skipped, and without the cleanup the durable
staging survives indefinitely. The `raise` matters as much as the `discard`: the caller still
has to learn the export failed.

Stage somewhere durable — a staging table, a temp file, a keyed batch — not a Python list.
Accumulating the export in memory to promote it later gives up the bound that made streaming
worth using, which is the trap this pattern invites.

Three properties of stubs matter for correctness:

- **Stubs are counted, not filtered.** Every member of the export accounts for exactly one
  record, stubs included, so a stub counts towards `MPT-Item-Count`. Do not drop stubs before
  the completeness check — a complete export would read as short. The safe way to drop them is
  [`skip_deleted`](#opting-out-of-deletion-stubs), which filters after that accounting has
  been fed, so a withheld stub still counts.
- **A stub is not a `DELETED` status.** A `DELETED` status is a domain state on a full,
  existing record, and stays a model. A stub marks a row that no longer exists at all and
  carries no state. Conflating them either loses a deletion or discards a live record.
- **A stub does not satisfy a record schema.** If you validate incoming payloads against a
  strict schema, branch on `DeletionStub` first and skip the record validation for stubs,
  rather than loosening the schema for records too.

Anything that reads a field other than `id` needs this branch. A loop that only reads
`order.id` is safe as written, because every streamed object carries an `id` — but it is one
edit away from not being safe.

#### Opting Out Of Deletion Stubs

A consumer that never ingests deletions — read-only analytics, an ad-hoc export — gains
nothing from the branch: it would drop the stubs and move on. Declare that with the
keyword-only `skip_deleted` flag instead of writing a branch that discards:

```python
for order in client.commerce.orders.stream(skip_deleted=True):
    print(order.id)
```

The flag is typed with overloads, so a type checker resolves `stream(skip_deleted=True)` to
`Iterator[Model]` — `AsyncIterator[Model]` on the async service — and an opted-out consumer
carries no union type through its own signatures. The default call keeps
`Iterator[Model | DeletionStub]` and the branch it forces.

Filtering happens at yield time, after the client's own bookkeeping, so the guarantees above
survive it:

- Completeness still counts the raw records ahead of the filter and still compares them with
  `MPT-Item-Count` once the body is consumed. A short stream raises
  `MPTStreamingIncompleteError` either way.
- A `progress` receiver still gets `item_processed` for every record, withheld stubs
  included, because the declared total counts stubs — a report fed only visible records
  would never reach 100%.

One consequence to plan for: under `skip_deleted=True` the number of objects your loop sees
no longer matches `MPT-Item-Count` when the snapshot contains stubs. Do not compare your own
count against the header in this mode. The client has already verified the full snapshot
arrived, which is the check that matters.

Opting out is a statement that deletions are irrelevant to this consumer, not a shortcut. A
job that mirrors the collection must keep the default and branch, or members deleted upstream
survive locally forever — the same silent divergence this obligation exists to prevent.

### 3. Restart, Do Not Resume

**Prevents:** splicing two different snapshots into one result set.

Resume is a contract non-goal. A retry is a new request, which opens a *new* membership
snapshot, so records from a failed attempt cannot be continued or appended to a later one.
Discard everything the failed attempt produced and restart from scratch:

```python
from mpt_api_client.exceptions import (
    MPTStreamingIncompleteError,
    MPTStreamingTruncatedError,
)

try:
    records = list(client.commerce.orders.stream())
except (MPTStreamingIncompleteError, MPTStreamingTruncatedError):
    records = list(client.commerce.orders.stream())  # a new snapshot, not a continuation
```

`MPTStreamingTruncatedError` is how a mid-stream failure arrives: the API signals an internal
failure by aborting the connection without completing the HTTP message, so the transport
failure is the failure signal. It is raised once the response has opened — usually after
records have reached your loop, but equally when the body dies before the first one. It is
not retry exhaustion: transparent retry runs while the response is being opened and cannot
re-request once the body has started, so `MPTMaxRetryError` stays reserved for a request that
never delivered a body at all.

The same rule covers `MPTStreamingIncompleteError`: whatever the cause, a failed export is
discarded whole and re-requested, never patched.

If restarting a large export is expensive, write records to a staging area keyed by the
attempt and promote it only after the stream completes without raising. That keeps the
discard cheap and keeps a failed attempt from reaching the records your consumers read.

## The Client-Timeout Trap

This is the failure most likely to be misdiagnosed, because a correctly working export looks
exactly like a broken one.

Phase one scans keys before a single byte of the body is written, and the platform's SLO
allows that to take up to **60 seconds** on a large export. During that time the connection
is established and the client is waiting for the response to start.

**It is the read timeout, not the connect timeout, that bounds a deferred first byte.** A
client tuned with a generous connect timeout and a short read timeout will abandon a working
export mid-scan and report a timeout that looks like a server failure.

`TransportSettings` exposes `stream_read_timeout` for exactly this. A streaming request's
read phase is bounded by the **larger** of `stream_read_timeout` and `read_timeout`, and
`stream_read_timeout` defaults to `120.0` — enough for the 60s SLO with headroom, where the
regular `read_timeout` default is not:

```python
from mpt_api_client import BearerTokenAuthentication, MPTClient, TransportSettings
from mpt_api_client.http import HTTPClient

client = MPTClient(
    http_client=HTTPClient(
        transport=TransportSettings(
            base_url="https://api.s1.show/public",
            timeout=20.0,
            connect_timeout=5.0,
            read_timeout=30.0,
            stream_read_timeout=180.0,
        ),
        authentication=BearerTokenAuthentication("<token>"),
    )
)
```

Three things to know about it:

- Because the larger value wins, raising `read_timeout` raises the streaming budget too, and
  streaming can never end up with the shorter of the two.
- It bounds a single read, not the whole export. No total-duration timeout is applied: an
  export runs for as long as the server keeps sending. Server-side keep-alives count as data
  and reset the read clock — blank lines in the line-delimited format, insignificant
  whitespace between tokens in the envelope.
- Lowering it below the SLO is the trap. If you tune timeouts down for a low-latency service
  and set `stream_read_timeout` from the same budget as your regular calls, large exports
  start failing while small ones keep working — which reads as a size-dependent server bug
  rather than a client setting.

Anything between your client and the platform needs the same treatment, and where the cut
falls decides which error you get:

- **Before the response headers arrive** — a proxy or load balancer whose first-byte timeout
  is shorter than the phase-one budget cuts the connection while the key scan is still
  running. Nothing has been committed yet, so transparent retry applies and the failure
  surfaces as `MPTMaxRetryError`, not as a truncated stream.
- **After the headers arrive** — a cut during the body is `MPTStreamingTruncatedError`, even
  if no record reached your loop, because the response had already committed its status.

See [Timeouts](usage.md#timeouts) for the full per-phase timeout model.

## Streaming Errors

All streaming-specific failures derive from `MPTStreamingError`, so one handler covers them:

| Exception | Raised when |
|---|---|
| `MPTStreamingNotEnabledError` | The response does not echo `MPT-Streaming`, so the body is an ordinary paged response |
| `MPTStreamingFormatMismatchError` | The response `Content-Type` names a media type other than the requested wire format |
| `MPTStreamingNotSupportedError` | `501` — the resource provides no streaming-capable execution strategy |
| `MPTStreamingNotAcceptableError` | `406` — the requested format cannot be served for this read mode |
| `MPTStreamingOverCapError` | `413` — the result set exceeds the configured `MaxExportKeys` cap |
| `MPTStreamingItemCountMissingError` | The response declares no usable `MPT-Item-Count`, so completeness cannot be verified |
| `MPTStreamingIncompleteError` | The fully consumed stream carried a different number of records than `MPT-Item-Count` declared |
| `MPTStreamingTruncatedError` | The connection was aborted mid-body, so the response ended before the HTTP message completed |

```python
import logging

from mpt_api_client.exceptions import MPTStreamingError

logger = logging.getLogger(__name__)

try:
    for order in client.commerce.orders.stream():
        print(order.id)
except MPTStreamingError as error:
    logger.error("Streaming unavailable: %s", error)
```

Split them by what a caller can do about them:

- **Request-shape and endpoint-support failures** — `MPTStreamingNotEnabledError`,
  `MPTStreamingFormatMismatchError`, `MPTStreamingNotSupportedError`,
  `MPTStreamingNotAcceptableError`, `MPTStreamingOverCapError` and
  `MPTStreamingItemCountMissingError`. Retrying the same call against the same endpoint fails
  the same way. Change the request, or fall back to `iterate()`. A `406` now genuinely can
  mean a format you asked for and the endpoint cannot serve, so check `stream_format` before
  assuming the endpoint is at fault.
- **Incomplete-export failures** — `MPTStreamingIncompleteError` and
  `MPTStreamingTruncatedError`. A retry can succeed, but only as a fresh export; see
  [Restart, Do Not Resume](#3-restart-do-not-resume).

`MPTStreamingNotEnabledError` and `MPTStreamingItemCountMissingError` are raised before the
body is read, so no partial data is consumed. The three HTTP-backed types also subclass
`MPTHttpError`, so existing `except MPTHttpError` handlers keep working and `status_code`
remains available. Any other HTTP status passes through unchanged.

A body the client cannot parse is not a streaming error at all but a `json.JSONDecodeError` —
a malformed record line in the line-delimited format, a malformed or unterminated envelope in
the envelope format. A body cut short usually loses records before it loses its closing
tokens, so a truncated export normally reports the more precise `MPTStreamingIncompleteError`
instead.

### Over-Cap Exports

The API answers `413` when the result set is larger than the configured `MaxExportKeys` cap.
`MPTStreamingOverCapError` keeps the `problem+json` body as structured data on `payload`
rather than flattening it into the message, because the configured cap is the value a caller
acts on:

```python
import logging

from mpt_api_client.exceptions import MPTStreamingOverCapError

logger = logging.getLogger(__name__)

try:
    records = list(client.commerce.orders.stream())
except MPTStreamingOverCapError as error:
    # The body names the configured cap. Read it defensively: payload is {} when the
    # response carried no JSON, and the member names are the server's, not the client's.
    cap = error.payload.get("maxExportKeys")
    logger.error("Export refused (configured cap: %s): %s", cap, error.payload)
    # A bounded retry is a different read: the first N of the sort order, not the export.
    records = list(client.commerce.orders.stream(limit=10_000))
```

`payload` is an empty mapping when the response carries no JSON body, so treat every member
as optional. The ways forward are the ones the body names: narrow the filter, set an explicit
`limit=N`, or split the export into key or date ranges.

Two things about that retry are worth being deliberate about:

- **A bounded retry does not get you the export.** `limit=N` returns the first `N` records of
  the sort order, and `MPT-Item-Count` reports the capped `K`, so the result is complete as a
  stream but is a prefix of the set you asked for. If you need all of it, narrow the filter or
  split by key or date range instead — those return the whole set in pieces.
- **Do not derive the limit from the cap.** A limit equal to `maxExportKeys` asks for the
  largest export the server will permit, which is the request that just failed for being too
  big to be useful. Pick a size the consumer can actually process; the cap tells you the
  request was refused, not what to ask for next.

## Async Streaming

The async form is the same contract over an async generator. Consume it inside a coroutine —
a top-level `async for` is a syntax error:

```python
import asyncio
import uuid

from mpt_api_client import AsyncMPTClient, BearerTokenAuthentication
from mpt_api_client.models import DeletionStub


async def export_orders() -> None:
    client = AsyncMPTClient.from_config(
        authentication=BearerTokenAuthentication("<token>"),
        base_url="https://api.s1.show/public",
    )
    attempt_id = uuid.uuid4().hex

    try:
        async for result in client.commerce.orders.stream():
            if isinstance(result, DeletionStub):
                await stage_delete(attempt_id, result.id)
            else:
                await stage_upsert(attempt_id, result)

        await promote(attempt_id)
    except Exception:
        await discard(attempt_id)
        raise


asyncio.run(export_orders())
```

Everything above applies unchanged: the same headers, the same completeness check, the same
stubs, the same restart rule. Only the `Async*` mixins and an `await`ed body differ.

## Reporting Progress

A long export gives no feedback by default. `stream()` accepts an optional `progress`
receiver, called once per consumed record — including a stub withheld by `skip_deleted` —
and once on completion:

```python
from mpt_api_client.models import ConsoleProgress

for order in client.commerce.orders.stream(progress=ConsoleProgress()):
    print(order.id)
```

The total is reported the same way in both wire formats: `set_total_items` is called exactly
once, with the declared `MPT-Item-Count`, when the response headers are verified — before
the first record — so `ConsoleProgress` renders a real percentage from the start of the
export. The envelope's `$meta.pagination.total` is contractually a mirror of that header and
is not re-reported.

The receiver is also where you capture the declared count when the payload is stored for
later verification, as [obligation 1](#1-verify-completeness-against-mpt-item-count)
describes. Implement the `Progress` protocol (or `AsyncProgress` for the async client) to
route progress somewhere other than the console.

## Related Documents

- [usage.md](usage.md): installation, client construction, timeouts, and general usage
- [architecture.md](architecture.md): where the streaming mixins and exceptions live
- [rql.md](rql.md): building the filters a stream applies
