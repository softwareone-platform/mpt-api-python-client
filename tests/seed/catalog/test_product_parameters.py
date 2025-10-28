from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.catalog.products_parameters import AsyncParametersService, Parameter
from seed.catalog.product_parameters import (
    build_parameter,
    create_parameter,
    get_parameter,
    init_parameter,
    seed_parameters,
)
from seed.context import Context

namespace = "catalog.parameter"


@pytest.fixture
def parameter() -> Parameter:
    return Parameter({"id": "param-123"})


@pytest.fixture
def parameters_service() -> AsyncMock:
    return AsyncMock(spec=AsyncParametersService)


@pytest.fixture
def vendor_client() -> AsyncMock:
    return MagicMock(spec=AsyncMPTClient)


async def test_get_parameter(
    context: Context, vendor_client: AsyncMock, parameter: Parameter
) -> None:
    context[f"{namespace}.id"] = parameter.id
    context["catalog.product.id"] = "product-123"
    service = AsyncMock(spec=AsyncParametersService)
    service.get.return_value = parameter
    vendor_client.catalog.products.product_parameters.return_value = service

    fetched_parameter = await get_parameter(context=context, mpt_vendor=vendor_client)

    assert fetched_parameter == parameter
    assert context.get(f"{namespace}.id") == parameter.id
    assert context.get(f"{namespace}[{parameter.id}]") == parameter


async def test_get_parameter_without_id(context: Context) -> None:
    maybe_parameter = await get_parameter(context=context)

    assert maybe_parameter is None


def test_build_parameter(context: Context) -> None:
    context["catalog.parameter_group.id"] = "group-123"

    parameter_payload: dict[str, Any] = build_parameter(context=context)

    assert parameter_payload["group"]["id"] == "group-123"


async def test_get_or_create_parameter_create_new(
    context: Context, vendor_client: AsyncMock, parameters_service: AsyncMock, parameter: Parameter
) -> None:
    context["catalog.product.id"] = "product-123"
    parameters_service.create.return_value = parameter
    vendor_client.catalog.products.product_parameters.return_value = parameters_service

    with (
        patch("seed.catalog.product_parameters.get_parameter", return_value=None),
        patch("seed.catalog.product_parameters.build_parameter", return_value=parameter),
    ):
        created_parameter = await init_parameter(context=context, mpt_vendor=vendor_client)

        assert created_parameter == parameter
        assert context.get(f"{namespace}.id") == parameter.id
        assert context.get(f"{namespace}[{parameter.id}]") == parameter


async def test_seed_parameters() -> None:
    with patch(
        "seed.catalog.product_parameters.init_parameter", new_callable=AsyncMock
    ) as mock_create:
        await seed_parameters()

        mock_create.assert_called_once()


async def test_create_parameter_success(
    context: Context, vendor_client: AsyncMock, parameter: Parameter
) -> None:
    context["catalog.product.id"] = "product-123"
    context["catalog.parameter_group.id"] = "group-123"
    service = AsyncMock(spec=AsyncParametersService)
    service.create.return_value = parameter
    vendor_client.catalog.products.product_parameters.return_value = service

    created = await create_parameter(context=context, mpt_vendor=vendor_client)

    assert created == parameter
    assert context.get("catalog.parameter.id") == parameter.id
    assert context.get(f"catalog.parameter[{parameter.id}]") == parameter


async def test_create_parameter_missing_product(context: Context, vendor_client: AsyncMock) -> None:
    context["catalog.parameter_group.id"] = "group-123"
    with pytest.raises(ValueError):
        await create_parameter(context=context, mpt_vendor=vendor_client)
