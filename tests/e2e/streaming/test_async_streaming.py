import pytest

from mpt_api_client.http.mixins import StreamFormat
from tests.e2e.streaming.memory_probe import (
    MAX_PEAK_GROWTH,
    MIN_BUFFERING_CONTRAST,
    SAMPLE_RECORDS,
    VOLUME_RECORDS,
    profile_async_streaming_memory,
)

# Every wire format the client offers, so a format added later is covered by construction
# rather than by someone remembering to extend this list.
STREAM_FORMATS = list(StreamFormat)


@pytest.mark.parametrize("stream_format", STREAM_FORMATS, ids=lambda fmt: fmt.name)
async def test_stream_at_volume_keeps_memory_bounded(async_large_collection, stream_format):
    result = await profile_async_streaming_memory(async_large_collection, stream_format)

    assert result.sample.records == SAMPLE_RECORDS
    assert result.volume.records == VOLUME_RECORDS
    assert result.buffered.records == VOLUME_RECORDS
    assert result.volume.peak_bytes <= result.sample.peak_bytes * MAX_PEAK_GROWTH
    assert result.buffered.peak_bytes >= result.volume.peak_bytes * MIN_BUFFERING_CONTRAST
