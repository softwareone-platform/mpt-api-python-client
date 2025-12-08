import pytest

from mpt_api_client.resources.catalog.products import Product
from seed.catalog.product import (  # noqa: WPS235
    create_document,
    create_item_group,
    create_parameter,
    create_parameter_group,
    create_product,
    create_product_item,
    create_template,
    create_terms,
    create_terms_variant,
    create_unit_of_measure,
)
from seed.context import Context


@pytest.fixture
def product():
    return Product({"id": "prod-123", "status": "Draft"})


@pytest.fixture
def context_with_product():
    context = Context()
    context["catalog.product.id"] = "prod-123"
    return context


async def test_create_product(mocker, context: Context, vendor_client, product):
    mpt_vendor = vendor_client
    mpt_vendor.catalog.products.create = mocker.AsyncMock(return_value=product)

    result = await create_product(mpt_vendor)

    assert result == product


async def test_create_template(mocker, vendor_client, context_with_product):
    context = context_with_product

    create_mock = mocker.AsyncMock(return_value={"id": "tmpl-1"})
    vendor_client.catalog.products.templates.return_value.create = create_mock

    result = await create_template(context, vendor_client)

    assert result == {"id": "tmpl-1"}
    create_mock.assert_awaited_once()


async def test_create_terms(mocker, vendor_client, context_with_product):
    context = context_with_product

    create_mock = mocker.AsyncMock(return_value={"id": "term-1"})
    vendor_client.catalog.products.terms.return_value.create = create_mock

    result = await create_terms(context, vendor_client)

    assert result == {"id": "term-1"}
    create_mock.assert_awaited_once()


async def test_create_terms_variant(mocker, vendor_client, context_with_product):
    context = context_with_product
    context["catalog.product.terms.id"] = "terms-123"

    create_mock = mocker.AsyncMock(return_value={"id": "variant-1"})
    vendor_client.catalog.products.terms.return_value.variants.return_value.create = create_mock

    result = await create_terms_variant(context, vendor_client)

    assert result == {"id": "variant-1"}


async def test_create_parameter_group(mocker, vendor_client, context_with_product):
    context = context_with_product

    create_mock = mocker.AsyncMock(return_value={"id": "pg-1"})
    vendor_client.catalog.products.parameter_groups.return_value.create = create_mock

    result = await create_parameter_group(context, vendor_client)

    assert result == {"id": "pg-1"}
    create_mock.assert_awaited_once()


async def test_create_parameter(mocker, vendor_client, context_with_product):
    context = context_with_product
    context["catalog.product.parameter_group.id"] = "pg-1"

    create_mock = mocker.AsyncMock(return_value={"id": "param-1"})
    vendor_client.catalog.products.parameters.return_value.create = create_mock

    result = await create_parameter(context, vendor_client)

    assert result == {"id": "param-1"}
    create_mock.assert_awaited_once()


async def test_create_document(mocker, vendor_client, context_with_product):
    context = context_with_product

    create_mock = mocker.AsyncMock(return_value={"id": "doc-1"})
    vendor_client.catalog.products.documents.return_value.create = create_mock

    result = await create_document(context, vendor_client)

    assert result == {"id": "doc-1"}


async def test_create_item_group(mocker, vendor_client, context_with_product):
    context = context_with_product

    create_mock = mocker.AsyncMock(return_value={"id": "ig-1"})
    vendor_client.catalog.products.item_groups.return_value.create = create_mock

    result = await create_item_group(context, vendor_client)

    assert result == {"id": "ig-1"}
    args, _ = create_mock.await_args
    payload = args[0]
    assert payload["product"]["id"] == "prod-123"


async def test_create_unit_of_measure(mocker, vendor_client):
    create_mock = mocker.AsyncMock(return_value={"id": "uom-1"})
    vendor_client.catalog.units_of_measure.create = create_mock

    result = await create_unit_of_measure(vendor_client)

    assert result == {"id": "uom-1"}
    create_mock.assert_awaited_once()


async def test_create_product_item(mocker, vendor_client, context_with_product):
    context_with_product["catalog.unit.id"] = "unit-1"
    context_with_product["catalog.product.item_group.id"] = "ig-1"

    create_mock = mocker.AsyncMock(return_value={"id": "item-1"})
    vendor_client.catalog.items.create = create_mock
    result = await create_product_item(context_with_product, vendor_client)

    assert result == {"id": "item-1"}
    args, _ = create_mock.await_args
    payload = args[0]
    assert payload["unit"]["id"] == "unit-1"
    assert payload["group"]["id"] == "ig-1"
    assert payload["product"]["id"] == "prod-123"
