import io
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mpt_api_client.resources.catalog.products import AsyncProductsService, Product
from seed.catalog.product import (
    get_product,
    init_product,
    publish_product,
    review_product,
    seed_product,
)
from seed.context import Context


@pytest.fixture
def product():
    return Product({"id": "prod-123", "status": "Draft"})


@pytest.fixture
def products_service():
    return AsyncMock(spec=AsyncProductsService)


async def test_get_product(context: Context, vendor_client, product, products_service) -> None:
    context["catalog.product.id"] = product.id
    products_service.get.return_value = product
    vendor_client.catalog.products = products_service

    fetched_product = await get_product(context=context, mpt_vendor=vendor_client)

    assert fetched_product == product
    assert context.get_resource("catalog.product", product.id) == product


async def test_get_product_without_id(context: Context) -> None:
    product = await get_product(context=context)
    assert product is None


async def test_get_or_create_product_create_new(
    context: Context, vendor_client, products_service, product
) -> None:
    products_service.create.return_value = product
    vendor_client.catalog.products = products_service
    fake_icon_bytes = io.BytesIO(b"fake image")

    with (
        patch("seed.catalog.product.get_product", return_value=None),
        patch("seed.catalog.product.icon", new=MagicMock()),
        patch("pathlib.Path.open", return_value=fake_icon_bytes),
    ):
        created = await init_product(context, mpt_vendor=vendor_client)
        assert created == product
        products_service.create.assert_called_once()


async def test_review_product_draft_status(
    context, products_service, vendor_client, product
) -> None:
    product.status = "Draft"
    products_service.review.return_value = product
    vendor_client.catalog.products = products_service
    with (
        patch("seed.catalog.product.get_product", return_value=product),
    ):
        reviewed = await review_product(context, mpt_vendor=vendor_client)
        assert reviewed == product
        products_service.review.assert_called_once()


async def test_review_product_non_draft_status(product) -> None:
    product.status = "Published"
    with patch("seed.catalog.product.get_product", return_value=product):
        unchanged = await review_product()
        assert unchanged == product


async def test_publish_product_reviewing_status(context, operations_client, product) -> None:
    product.status = "Reviewing"
    operations_client.catalog.products.publish = AsyncMock(return_value=product)
    with (
        patch("seed.catalog.product.get_product", return_value=product),
    ):
        published = await publish_product(context, mpt_operations=operations_client)
        assert published == product
        operations_client.catalog.products.publish.assert_called_once()


async def test_publish_product_non_reviewing_status(product) -> None:
    product.status = "Draft"
    with patch("seed.catalog.product.get_product", return_value=product):
        unchanged = await publish_product()
        assert unchanged == product


async def test_seed_product_sequence() -> None:
    with (
        patch("seed.catalog.product.init_product", new_callable=AsyncMock) as mock_create,
        patch("seed.catalog.product.review_product", new_callable=AsyncMock) as mock_review,
        patch("seed.catalog.product.publish_product", new_callable=AsyncMock) as mock_publish,
    ):
        await seed_product()
        mock_create.assert_called_once()
        mock_review.assert_called_once()
        mock_publish.assert_called_once()
