import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [
    pytest.mark.flaky,
    pytest.mark.skip(reason="Skipped per MPT-18373 request"),
]


async def test_get_parameter_group_parameter(
    async_parameter_group_parameters_service, async_created_parameter_group_parameter
):
    result = await async_parameter_group_parameters_service.get(
        async_created_parameter_group_parameter.id
    )

    assert result.id == async_created_parameter_group_parameter.id


async def test_list_parameter_group_parameters(
    async_parameter_group_parameters_service, async_created_parameter_group_parameter
):
    result = await async_parameter_group_parameters_service.fetch_page(limit=20)

    assert any(parameter.id == async_created_parameter_group_parameter.id for parameter in result)


def test_create_parameter_group_parameter(async_created_parameter_group_parameter):
    result = async_created_parameter_group_parameter

    assert result is not None


async def test_update_parameter_group_parameter(
    async_parameter_group_parameters_service, async_created_parameter_group_parameter
):
    update_data = {"displayOrder": 101}

    result = await async_parameter_group_parameters_service.update(
        async_created_parameter_group_parameter.id,
        update_data,
    )

    assert result.id == async_created_parameter_group_parameter.id
    assert result.to_dict().get("displayOrder") == update_data["displayOrder"]


async def test_delete_parameter_group_parameter(
    async_parameter_group_parameters_service, async_created_parameter_group_parameter
):
    await async_parameter_group_parameters_service.delete(
        async_created_parameter_group_parameter.id
    )  # act


async def test_not_found(
    async_parameter_group_parameters_service, invalid_parameter_group_parameter_id
):
    with pytest.raises(MPTAPIError):
        await async_parameter_group_parameters_service.get(invalid_parameter_group_parameter_id)
