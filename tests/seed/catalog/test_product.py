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
def products_service(mocker):
    return mocker.Mock(spec=AsyncProductsService)


async def test_get_product(context: Context, vendor_client, product, products_service):
    context["catalog.product.id"] = product.id
    products_service.get.return_value = product
    vendor_client.catalog.products = products_service

    result = await get_product(context=context, mpt_vendor=vendor_client)

    assert result == product
    assert context.get_resource("catalog.product", product.id) == product


async def test_get_product_without_id(context: Context):
    result = await get_product(context=context)

    assert result is None


async def test_get_or_create_product_create_new(  # noqa: WPS211
    context: Context, vendor_client, products_service, product, fs, mocker
):
    products_service.create.return_value = product
    vendor_client.catalog.products = products_service
    fs.create_file(
        "/mpt_api_client/seed/catalog/FIL-9920-4780-9379.png", contents=b"fake_icon_bytes"
    )
    mock_get_product = mocker.patch(
        "seed.catalog.product.get_product", new_callable=mocker.AsyncMock
    )
    mock_get_product.return_value = None
    result = await init_product(context=context, mpt_vendor=vendor_client)
    assert result == product
    products_service.create.assert_called_once()


async def test_review_product_draft_status(
    context, products_service, vendor_client, product, mocker
):
    product.status = "Draft"
    products_service.review.return_value = product
    vendor_client.catalog.products = products_service
    mocker.patch("seed.catalog.product.get_product", return_value=product)
    result = await review_product(context, mpt_vendor=vendor_client)
    assert result == product
    products_service.review.assert_called_once()


async def test_review_product_non_draft_status(product, mocker):
    product.status = "Published"
    mocker.patch("seed.catalog.product.get_product", return_value=product)
    result = await review_product()
    assert result == product


async def test_publish_product_reviewing_status(context, operations_client, product, mocker):
    product.status = "Reviewing"
    operations_client.catalog.products.publish = mocker.AsyncMock(return_value=product)
    mocker.patch("seed.catalog.product.get_product", return_value=product)
    result = await publish_product(context, mpt_operations=operations_client)
    assert result == product
    operations_client.catalog.products.publish.assert_called_once()


async def test_publish_product_non_reviewing_status(product, mocker):
    product.status = "Draft"
    mocker.patch("seed.catalog.product.get_product", return_value=product)
    result = await publish_product()
    assert result == product


async def test_seed_product_sequence(mocker):
    mock_create = mocker.patch("seed.catalog.product.init_product", new_callable=mocker.AsyncMock)
    mock_review = mocker.patch("seed.catalog.product.review_product", new_callable=mocker.AsyncMock)
    mock_publish = mocker.patch(
        "seed.catalog.product.publish_product", new_callable=mocker.AsyncMock
    )
    await seed_product()  # act
    mock_create.assert_called_once()
    mock_review.assert_called_once()
    mock_publish.assert_called_once()
