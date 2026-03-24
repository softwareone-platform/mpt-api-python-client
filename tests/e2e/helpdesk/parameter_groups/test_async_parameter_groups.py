import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [
    pytest.mark.flaky,
    pytest.mark.skip(reason="Skipped per MPT-18373 request"),
]


async def test_get_parameter_group(async_parameter_groups_service, async_created_parameter_group):
    result = await async_parameter_groups_service.get(async_created_parameter_group.id)

    assert result.id == async_created_parameter_group.id


async def test_list_parameter_groups(async_parameter_groups_service):
    result = await async_parameter_groups_service.fetch_page(limit=1)

    assert len(result) > 0


def test_create_parameter_group(async_created_parameter_group):
    result = async_created_parameter_group

    assert result is not None


async def test_update_parameter_group(
    async_parameter_groups_service, async_created_parameter_group, short_uuid
):
    update_data = {"description": f"e2e update {short_uuid}"}

    result = await async_parameter_groups_service.update(
        async_created_parameter_group.id, update_data
    )

    assert result.id == async_created_parameter_group.id
    assert result.to_dict().get("description") == update_data["description"]


async def test_delete_parameter_group(
    async_parameter_groups_service, async_created_parameter_group
):
    await async_parameter_groups_service.delete(async_created_parameter_group.id)  # act


async def test_not_found(async_parameter_groups_service, invalid_parameter_group_id):
    with pytest.raises(MPTAPIError):
        await async_parameter_groups_service.get(invalid_parameter_group_id)
