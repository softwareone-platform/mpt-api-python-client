import pytest

from tests.e2e.streaming.memory_probe import VOLUME_RECORDS


def _require_volume(page):
    total = page.meta.pagination.total if page.meta else 0
    if total < VOLUME_RECORDS:
        pytest.fail(
            f"Catalog items hold {total} records on this environment, fewer than the "
            f"{VOLUME_RECORDS} this coverage streams. The constant-memory assertion is "
            "only meaningful at volume, so this is a data problem, not a client failure."
        )


@pytest.fixture
def large_collection(mpt_ops):
    service = mpt_ops.catalog.items
    _require_volume(service.fetch_page(limit=1))
    return service


@pytest.fixture
async def async_large_collection(async_mpt_ops):
    service = async_mpt_ops.catalog.items
    _require_volume(await service.fetch_page(limit=1))
    return service
