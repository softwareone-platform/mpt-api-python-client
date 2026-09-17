import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


async def test_get_service(async_services_service, service_id):
    result = await async_services_service.get(service_id)

    assert result.id == service_id


async def test_get_service_not_found(async_services_service, invalid_service_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_services_service.get(invalid_service_id)


async def test_list_services(async_services_service):
    limit = 10

    result = await async_services_service.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_services(async_services_service, service_id):
    await assert_async_service_filter_with_iterate(async_services_service, service_id, None)  # act
