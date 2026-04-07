import pytest

from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


@pytest.mark.skip(reason="returns 500 error")
async def test_create_extension_instance(async_extension_instances_service, instance_data):
    result = await async_extension_instances_service.create(instance_data)

    assert result.external_id == instance_data["externalId"]


async def test_filter_extension_instances(async_extension_instances_service, instance_id):
    await assert_async_service_filter_with_iterate(
        async_extension_instances_service, instance_id, None
    )  # act


async def test_get_extension_instance(async_extension_instances_service, instance_id):
    result = await async_extension_instances_service.get(instance_id)

    assert result.id == instance_id
