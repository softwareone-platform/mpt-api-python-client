import pytest

from mpt_api_client.models import DeletionStub
from tests.e2e.streaming.race import (
    BOUNDED_EXPORT,
    EARLY_CLOSE_RECORDS,
    OLDEST_FIRST,
    AsyncCountingProgress,
    async_race_delete_mid_stream,
    async_read_then_close,
)

pytestmark = [pytest.mark.flaky]


async def test_async_stream_stub_for_deleted_row(
    async_mpt_ops, async_mpt_vendor, async_deletable_product
):
    streamed_products = async_mpt_ops.catalog.products.order_by(OLDEST_FIRST).stream_snapshot()

    result = await async_race_delete_mid_stream(
        streamed_products, async_mpt_vendor.catalog.products, async_deletable_product.id
    )

    assert result.objects_for_row == [DeletionStub(id=async_deletable_product.id)]


async def test_async_stream_withholds_counted_stub(
    async_mpt_ops, async_mpt_vendor, async_deletable_product
):
    progress = AsyncCountingProgress()
    streamed_products = async_mpt_ops.catalog.products.order_by(OLDEST_FIRST).stream_snapshot(
        skip_deleted=True, progress=progress
    )

    result = await async_race_delete_mid_stream(
        streamed_products, async_mpt_vendor.catalog.products, async_deletable_product.id
    )

    # The declared count equals the records processed, while the caller sees one fewer:
    # the stub was counted but withheld. That is what keeps the MPT-Item-Count
    # verification passing, so reaching this line proves it did not raise.
    assert (result.objects_for_row, progress.totals, result.yielded) == (
        [],
        [progress.processed],
        progress.processed - 1,
    )


async def test_async_stream_reports_declared_count(async_mpt_ops):
    progress = AsyncCountingProgress()
    streamed_products = async_mpt_ops.catalog.products.stream_snapshot(
        limit=BOUNDED_EXPORT, progress=progress
    )

    result = len([streamed async for streamed in streamed_products])

    # Reported exactly once, before the records, and matching what the stream carried.
    assert (progress.totals, result) == ([BOUNDED_EXPORT], BOUNDED_EXPORT)


async def test_async_stream_early_close_does_not_raise(async_mpt_ops):
    progress = AsyncCountingProgress()
    streamed_products = async_mpt_ops.catalog.products.stream_snapshot(
        limit=BOUNDED_EXPORT, progress=progress
    )

    result = await async_read_then_close(streamed_products, EARLY_CLOSE_RECORDS)

    # Deliberately stopping short of the declared count is not an incomplete export.
    assert (result, progress.totals) == (EARLY_CLOSE_RECORDS, [BOUNDED_EXPORT])
