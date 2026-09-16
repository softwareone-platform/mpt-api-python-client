import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


async def test_get_pair(async_pairs_service, pair_id):
    result = await async_pairs_service.get(pair_id)

    assert result.id == pair_id


async def test_get_pair_not_found(async_pairs_service):
    bogus_id = "FXP-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_pairs_service.get(bogus_id)


async def test_filter_pairs(async_pairs_service, pair_id):
    await assert_async_service_filter_with_iterate(async_pairs_service, pair_id, None)  # act
