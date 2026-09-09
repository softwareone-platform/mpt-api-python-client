from typing import NamedTuple

# Ascending creation order puts a just-created row last in the export, so the whole stream
# is hydrated before the platform reaches it and a delete issued early lands inside the
# window between the phase-1 key snapshot and the phase-2 read of that key.
OLDEST_FIRST = "audit.created.at"

# A bounded export the server can satisfy cheaply: under an explicit limit the declared
# count is min(matches, N), and the products collection holds far more than this.
BOUNDED_EXPORT = 50

# Far fewer than BOUNDED_EXPORT, so an early close genuinely leaves records unread.
EARLY_CLOSE_RECORDS = 5


class StreamRace(NamedTuple):
    """What a stream produced for the row that was deleted while it was open."""

    objects_for_row: list
    yielded: int


class CountingProgress:
    """Progress fake recording the declared totals and counting the records processed.

    `stream()` reports the declared `MPT-Item-Count` once, before the first record, and
    counts every record it processes including a stub withheld by ``skip_deleted``.
    """

    def __init__(self):
        self.totals = []
        self.processed = 0

    def set_total_items(self, total):
        self.totals.append(total)

    def item_processed(self):
        self.processed += 1

    def completed(self):
        """Ignored: completion is proven by the stream returning without raising."""


class AsyncCountingProgress:
    """Async counterpart of `CountingProgress`."""

    def __init__(self):
        self.totals = []
        self.processed = 0

    async def set_total_items(self, total):
        self.totals.append(total)

    async def item_processed(self):
        self.processed += 1

    async def completed(self):
        """Ignored: completion is proven by the stream returning without raising."""


def race_delete_mid_stream(stream, resource_service, resource_id):
    """Consume a stream, hard-deleting `resource_id` once the first record has arrived.

    Deleting after the first record is both safe and necessary: the response headers are
    out by then, so the export's key snapshot already contains the row. Deleting before the
    stream opens leaves the row out of the snapshot entirely and produces no stub.
    """
    objects_for_row = []
    yielded = 0
    deleted = False
    for streamed in stream:
        if not deleted:
            resource_service.delete(resource_id)
            deleted = True
        yielded += 1
        if streamed.id == resource_id:
            objects_for_row.append(streamed)
    return StreamRace(objects_for_row, yielded)


async def async_race_delete_mid_stream(stream, resource_service, resource_id):
    """Async counterpart of `race_delete_mid_stream`."""
    objects_for_row = []
    yielded = 0
    deleted = False
    async for streamed in stream:
        if not deleted:
            await resource_service.delete(resource_id)
            deleted = True
        yielded += 1
        if streamed.id == resource_id:
            objects_for_row.append(streamed)
    return StreamRace(objects_for_row, yielded)


def read_then_close(stream, record_count):
    """Read `record_count` records, then close the stream before it is exhausted.

    Closing early must not report an incomplete export: the completeness check applies
    only to a stream consumed to the end, so a deliberate `break` is not a failure.
    """
    records_read = 0
    for _ in stream:
        records_read += 1
        if records_read == record_count:
            break
    stream.close()
    return records_read


async def async_read_then_close(stream, record_count):
    """Async counterpart of `read_then_close`."""
    records_read = 0
    async for _ in stream:
        records_read += 1
        if records_read == record_count:
            break
    await stream.aclose()
    return records_read
