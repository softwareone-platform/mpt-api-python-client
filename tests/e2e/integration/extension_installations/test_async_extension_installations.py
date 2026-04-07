import pytest

from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


async def test_filter_extension_installations(
    async_extension_installations_service, installation_id
):
    await assert_async_service_filter_with_iterate(
        async_extension_installations_service, installation_id, None
    )  # act


async def test_get_extension_installation(async_extension_installations_service, installation_id):
    result = await async_extension_installations_service.get(installation_id)

    assert result.id == installation_id
