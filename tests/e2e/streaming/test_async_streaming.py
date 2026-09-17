from tests.e2e.streaming.memory_probe import (
    MAX_PEAK_GROWTH,
    MIN_BUFFERING_CONTRAST,
    SAMPLE_RECORDS,
    VOLUME_RECORDS,
    profile_async_streaming_memory,
)


async def test_stream_at_volume_keeps_memory_bounded(async_large_collection):
    result = await profile_async_streaming_memory(async_large_collection)

    assert result.sample.records == SAMPLE_RECORDS
    assert result.volume.records == VOLUME_RECORDS
    assert result.buffered.records == VOLUME_RECORDS
    assert result.volume.peak_bytes <= result.sample.peak_bytes * MAX_PEAK_GROWTH
    assert result.buffered.peak_bytes >= result.volume.peak_bytes * MIN_BUFFERING_CONTRAST
