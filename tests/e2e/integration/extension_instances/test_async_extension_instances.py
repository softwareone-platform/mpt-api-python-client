import pytest

from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


@pytest.mark.skip(reason="creates real resources; run manually only")
async def test_create_extension_instance(async_extension_instances_service, instance_data):
    result = await async_extension_instances_service.create(instance_data)

    assert result.external_id == instance_data["externalId"]


async def test_filter_extension_instances(async_extension_instances_service, extension_id):
    await assert_async_service_filter_with_iterate(
        async_extension_instances_service, extension_id, None
    )  # act
