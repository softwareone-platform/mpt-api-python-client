"""Measurement protocol behind the constant-memory streaming coverage.

`stream()` claims memory stays bounded no matter how many records the export carries.
Proving that needs two comparisons on the same live data, which is what
`profile_streaming_memory` collects in one pass:

- the allocation peak of a small export against the peak of an export ten times longer,
  so a peak that scales with the record count fails;
- the peak of the streamed read against the peak of buffering the same export, so the
  measurement is shown to be sensitive enough to see buffering at this volume.

Every measured window covers a whole read, from the request being opened to the body being
exhausted. That matters: an implementation that buffers does so before it yields its first
record, so a window that started mid-stream would measure only the walk over an
already-materialised list and see nothing wrong.

Peaks come from `tracemalloc`, which counts Python allocations rather than process resident
size, so the numbers do not move with allocator or kernel behaviour. Every peak is reported
net of the memory already live when its window opens, and each window starts with a
collection, so an object released by an earlier read is never charged to a later one.

The profile is taken per wire format, because the property has to hold for each of them
separately and they reach it by different routes: `JSONL` reads one record per line, while
`JSON` parses records out of the `{$meta, data}` envelope incrementally. The envelope is the
easier one to get wrong, since the obvious implementation deserializes the whole body first.
"""

import gc
import tracemalloc
from collections.abc import Awaitable, Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any

from mpt_api_client.http.mixins import StreamFormat

# Records exported before the first measured window, so connection setup, lazy imports and
# the first read buffers are paid for outside every comparison. This is a separate read,
# not a prologue of a measured one, so nothing can hide in it.
WARMUP_RECORDS = 500
# Records exported by the short read that the volume read is compared against.
SAMPLE_RECORDS = 2000
# Records exported by the volume read: ten times the short read, and enough that buffering
# the same export costs tens of megabytes.
VOLUME_RECORDS = 20000
# How much the volume read's peak may exceed the short read's. Ten times the records must not
# cost materially more memory. A buffering read scales with the record count, so it lands near
# 10x here and is caught with a wide margin. The ceiling sits well above the highest ratio
# measured on a healthy stream (1.71, from an async run whose short window happened to peak
# low) because the short window is the noisier of the two: an unusually cheap sample inflates
# the ratio, and this must never fail on that alone.
MAX_PEAK_GROWTH = 4.0
# How much more buffering the export must peak than streaming it. Guards against a vacuous
# pass: on a dataset too small to matter, the two reads would cost about the same.
MIN_BUFFERING_CONTRAST = 20.0

# One traced frame per allocation: the call site is never reported, so tracing costs less.
TRACE_FRAMES = 1


@dataclass(frozen=True)
class PeakReading:
    records: int
    peak_bytes: int


@dataclass(frozen=True)
class StreamingMemoryProfile:
    sample: PeakReading
    volume: PeakReading
    buffered: PeakReading


@contextmanager
def tracing_allocations() -> Iterator[None]:
    gc.collect()
    tracemalloc.start(TRACE_FRAMES)
    try:
        yield
    finally:
        tracemalloc.stop()


def measure_peak(read: Callable[[], int]) -> PeakReading:
    gc.collect()
    tracemalloc.reset_peak()
    baseline_bytes = tracemalloc.get_traced_memory()[0]
    records = read()
    peak_bytes = tracemalloc.get_traced_memory()[1] - baseline_bytes
    return PeakReading(records=records, peak_bytes=peak_bytes)


async def measure_peak_async(read: Callable[[], Awaitable[int]]) -> PeakReading:
    gc.collect()
    tracemalloc.reset_peak()
    baseline_bytes = tracemalloc.get_traced_memory()[0]
    records = await read()
    peak_bytes = tracemalloc.get_traced_memory()[1] - baseline_bytes
    return PeakReading(records=records, peak_bytes=peak_bytes)


def drain_stream(service: Any, limit: int, stream_format: StreamFormat) -> int:
    """Stream `limit` records, retaining none.

    The stream is consumed to exhaustion, which is what triggers its completeness check.
    """
    return sum(1 for _ in service.stream(limit=limit, stream_format=stream_format))


async def drain_stream_async(service: Any, limit: int, stream_format: StreamFormat) -> int:
    """Stream `limit` records, retaining none.

    The stream is consumed to exhaustion, which is what triggers its completeness check.
    """
    # WPS519 would have the records collected and counted, which is the buffering this
    # measurement exists to rule out.
    consumed = 0
    records = service.stream(limit=limit, stream_format=stream_format)
    async for _ in records:  # noqa: WPS519
        consumed += 1
    return consumed


def buffer_export(service: Any, stream_format: StreamFormat) -> int:
    """Materialise a whole export, the buffering read the streamed read is compared with."""
    return len(list(service.stream(limit=VOLUME_RECORDS, stream_format=stream_format)))


async def buffer_export_async(service: Any, stream_format: StreamFormat) -> int:
    """Materialise a whole export, the buffering read the streamed read is compared with."""
    records = service.stream(limit=VOLUME_RECORDS, stream_format=stream_format)
    return len([record async for record in records])


def profile_streaming_memory(service: Any, fmt: StreamFormat) -> StreamingMemoryProfile:
    with tracing_allocations():
        drain_stream(service, WARMUP_RECORDS, fmt)
        sample = measure_peak(lambda: drain_stream(service, SAMPLE_RECORDS, fmt))
        volume = measure_peak(lambda: drain_stream(service, VOLUME_RECORDS, fmt))
        buffered = measure_peak(lambda: buffer_export(service, fmt))
    return StreamingMemoryProfile(sample=sample, volume=volume, buffered=buffered)


async def profile_async_streaming_memory(service: Any, fmt: StreamFormat) -> StreamingMemoryProfile:
    with tracing_allocations():
        await drain_stream_async(service, WARMUP_RECORDS, fmt)
        sample = await measure_peak_async(lambda: drain_stream_async(service, SAMPLE_RECORDS, fmt))
        volume = await measure_peak_async(lambda: drain_stream_async(service, VOLUME_RECORDS, fmt))
        buffered = await measure_peak_async(lambda: buffer_export_async(service, fmt))
    return StreamingMemoryProfile(sample=sample, volume=volume, buffered=buffered)
