from unittest.mock import AsyncMock, patch

import pytest

from mpt_api_client.resources.catalog.products_parameter_groups import (
    AsyncParameterGroupsService,
    ParameterGroup,
)
from seed.catalog.product_parameters_group import (
    build_parameter_group,
    create_parameter_group,
    get_parameter_group,
    init_parameter_group,
    seed_parameter_group,
)
from seed.context import Context


@pytest.fixture
def parameter_group() -> ParameterGroup:
    return ParameterGroup({"id": "param-group-123"})


@pytest.fixture
def parameter_groups_service():
    return AsyncMock(spec=AsyncParameterGroupsService)


async def test_get_parameter_group(
    context: Context, vendor_client, parameter_groups_service, parameter_group
) -> None:
    context["catalog.product.parameter_group.id"] = parameter_group.id
    context["catalog.product.id"] = "product-123"
    parameter_groups_service.get.return_value = parameter_group
    vendor_client.catalog.products.parameter_groups.return_value = parameter_groups_service

    result = await get_parameter_group(context=context, mpt_vendor=vendor_client)

    assert result == parameter_group
    assert context.get("catalog.product.parameter_group.id") == parameter_group.id
    assert context.get(f"catalog.product.parameter_group[{parameter_group.id}]") == parameter_group


async def test_get_parameter_group_without_id(context: Context) -> None:
    result = await get_parameter_group(context=context)

    assert result is None


def test_build_parameter_group(context: Context) -> None:
    parameter_group_payload = build_parameter_group(context=context)

    result = isinstance(parameter_group_payload, dict)

    assert result is True


async def test_get_or_create_parameter_group_create_new(
    context: Context, vendor_client, parameter_groups_service, parameter_group
) -> None:
    context["catalog.product.id"] = "product-123"

    with (
        patch(
            "seed.catalog.product_parameters_group.get_parameter_group", return_value=None
        ) as get_mock,
        patch(
            "seed.catalog.product_parameters_group.create_parameter_group",
            return_value=parameter_group,
        ) as create_mock,
    ):
        created_parameter_group = await init_parameter_group(
            context=context, mpt_vendor=vendor_client
        )

        assert created_parameter_group == parameter_group
        get_mock.assert_called_once()
        create_mock.assert_called_once()


async def test_create_parameter_group_success(
    context: Context, vendor_client, parameter_group
) -> None:
    context["catalog.product.id"] = "product-123"
    service = AsyncMock(spec=AsyncParameterGroupsService)
    service.create.return_value = parameter_group
    vendor_client.catalog.products.parameter_groups.return_value = service

    created = await create_parameter_group(context=context, mpt_vendor=vendor_client)

    assert created == parameter_group
    assert context.get("catalog.product.parameter_group.id") == parameter_group.id
    assert context.get(f"catalog.product.parameter_group[{parameter_group.id}]") == parameter_group


async def test_seed_parameter_group() -> None:
    with patch(
        "seed.catalog.product_parameters_group.init_parameter_group",
        new_callable=AsyncMock,
    ) as mock_create:
        await seed_parameter_group()

        mock_create.assert_called_once()
