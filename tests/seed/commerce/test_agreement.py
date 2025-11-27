import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.commerce.agreements import Agreement, AsyncAgreementsService
from seed.commerce.agreement import (
    build_agreement,
    get_agreement,
    init_agreement,
    seed_agreement,
)


@pytest.fixture
def agreement():
    return Agreement({
        "id": "agreement-123",
        "name": "Test Agreement",
    })


@pytest.fixture
def agreements_service():
    return AsyncMock(spec=AsyncAgreementsService)


@pytest.fixture
def ops_client() -> AsyncMock:
    return AsyncMock(spec=AsyncMPTClient)


async def test_get_agreement(context, ops_client, agreement) -> None:
    context["commerce.agreement.id"] = agreement.id
    service = AsyncMock(spec=AsyncAgreementsService)
    service.get.return_value = agreement
    ops_client.commerce.agreements.return_value = service

    result = await get_agreement(context=context, mpt_operations=ops_client)

    assert result == agreement
    service.get.assert_called_once_with(context["commerce.agreement.id"])


async def test_get_agreement_without_id(context) -> None:
    result = await get_agreement(context=context)

    assert result is None


def test_set_agreement(context, agreement) -> None:
    result = init_agreement(agreement, context=context)

    assert result == agreement
    assert context["commerce.agreement.id"] == agreement.id
    assert context.get_resource("commerce.agreement", agreement.id) == agreement


def test_build_agreement(context) -> None:
    context["accounts.account.id"] = "account-123"
    context["accounts.seller.id"] = "seller-123"
    context["accounts.buyer.id"] = "buyer-123"
    context["accounts.licensee.id"] = "licensee-123"
    context["catalog.product.id"] = "product-123"
    context["commerce.product.template.id"] = "template-123"

    result = pytest.run(asyncio.run(build_agreement(context=context)))

    assert result["name"] == "E2E Seeded Agreement"
    assert result["status"] == "Active"
    assert result["client"]["id"] == "account-123"
    assert result["seller"]["id"] == "seller-123"
    assert result["buyer"]["id"] == "buyer-123"
    assert result["licensee"]["id"] == "licensee-123"
    assert result["product"]["id"] == "product-123"


async def test_get_or_create_agreement_create_new(
    context, ops_client, agreements_service, agreement
) -> None:
    context["accounts.account.id"] = "account-123"
    context["accounts.seller.id"] = "seller-123"
    context["accounts.buyer.id"] = "buyer-123"
    context["accounts.licensee.id"] = "licensee-123"
    context["catalog.product.id"] = "product-123"
    context["commerce.product.template.id"] = "template-123"
    agreements_service.create.return_value = agreement
    ops_client.commerce.agreements.return_value = agreements_service

    with (
        patch("seed.commerce.agreement.get_agreement", return_value=None),
        patch("seed.commerce.agreement.build_agreement", return_value=agreement),
        patch("seed.commerce.agreement.init_agreement", return_value=agreement) as set_agreement,
    ):
        result = await init_agreement(context=context, mpt_operations=ops_client)

    assert result == agreement
    agreements_service.create.assert_called_once()
    set_agreement.assert_called_once()


async def test_seed_agreement() -> None:
    with (
        patch(
            "seed.commerce.agreement.init_agreement", new_callable=AsyncMock
        ) as mock_init_agreement,
    ):
        await seed_agreement()  # act

        mock_init_agreement.assert_called_once()
