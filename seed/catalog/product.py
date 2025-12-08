import logging
import uuid

from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.catalog.items import Item
from mpt_api_client.resources.catalog.product_term_variants import TermVariant
from mpt_api_client.resources.catalog.product_terms import Term
from mpt_api_client.resources.catalog.products import Product
from mpt_api_client.resources.catalog.products_documents import Document
from mpt_api_client.resources.catalog.products_item_groups import ItemGroup
from mpt_api_client.resources.catalog.products_parameter_groups import ParameterGroup
from mpt_api_client.resources.catalog.products_parameters import Parameter
from mpt_api_client.resources.catalog.products_templates import Template
from mpt_api_client.resources.catalog.units_of_measure import UnitOfMeasure
from seed.assets.assets import ICON, PDF
from seed.container import Container
from seed.context import Context
from seed.helper import init_resource, require_context_id

logger = logging.getLogger(__name__)


@inject
async def create_product(
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
) -> Product:
    """Creates a product."""
    logger.debug("Creating product ...")
    with ICON.open("rb") as icon_fd:
        return await mpt_vendor.catalog.products.create(
            {"name": "E2E Seeded", "website": "https://www.example.com"}, file=icon_fd
        )


async def seed_product(
    context: Context = Provide[Container.context],
) -> None:
    """Seed product data."""
    logger.debug("Seeding catalog.product ...")
    await init_resource("catalog.product.id", create_product)
    await init_resource("catalog.unit.id", create_unit_of_measure)
    await init_resource("catalog.product.item_group.id", create_item_group)
    await init_resource("catalog.product.item.id", create_product_item)
    await init_resource("catalog.product.document.id", create_document)
    await init_resource("catalog.product.parameter_group.id", create_parameter_group)
    await init_resource("catalog.product.parameter.id", create_parameter)
    await init_resource("catalog.product.template.id", create_template)
    await init_resource("catalog.product.terms.id", create_terms)
    await init_resource("catalog.product.terms.variant.id", create_terms_variant)
    logger.debug("Seeded catalog.product completed.")


async def create_terms_variant(
    context: Context = Provide[Container.context],
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
) -> TermVariant:
    """Creates a product terms variant."""
    term_variant_data = {
        "name": "E2E seeding",
        "description": "Test variant description",
        "languageCode": "en-gb",
        "type": "File",
        "assetUrl": "",
    }
    product_id = require_context_id(context, "catalog.product.id", "creating product terms variant")
    terms_id = require_context_id(
        context, "catalog.product.terms.id", "creating product terms variant"
    )
    with PDF.open("rb") as pdf_fd:
        return (
            await mpt_vendor.catalog.products.terms(product_id)
            .variants(terms_id)
            .create(term_variant_data, file=pdf_fd)
        )


async def create_template(
    context: Context = Provide[Container.context],
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
) -> Template:
    """Creates a product template."""
    template_data = {
        "name": "E2E Seeding",
        "description": "A template for testing",
        "content": "template content",
        "type": "OrderProcessing",
    }
    product_id = require_context_id(context, "catalog.product.id", "creating product template")
    return await mpt_vendor.catalog.products.templates(product_id).create(template_data)


async def create_terms(
    context: Context = Provide[Container.context],
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
) -> Term:
    """Creates a product terms."""
    product_id = require_context_id(context, "catalog.product.id", "creating product terms")
    return await mpt_vendor.catalog.products.terms(product_id).create({
        "name": "E2E seeded",
        "description": "E2E seeded",
    })


async def create_parameter_group(
    context: Context = Provide[Container.context],
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
) -> ParameterGroup:
    """Creates a product parameter group."""
    product_id = require_context_id(
        context, "catalog.product.id", "creating product parameter group"
    )
    return await mpt_vendor.catalog.products.parameter_groups(product_id).create({
        "name": "E2E Seeded",
        "label": "E2E Seeded",
        "displayOrder": 100,
    })


async def create_parameter(
    context: Context = Provide[Container.context],
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
) -> Parameter:
    """Creates a product parameter."""
    parameter_group_id = require_context_id(
        context, "catalog.product.parameter_group.id", "creating product parameter"
    )
    parameter_data = {
        "constraints": {"hidden": False, "readonly": False, "required": False},
        "description": "E2E seeded",
        "displayOrder": 100,
        "name": "E2E seeded",
        "phase": "Order",
        "scope": "Order",
        "type": "SingleLineText",
        "context": "Purchase",
        "options": {
            "hintText": "e2e seeded",
            "defaultValue": "default value",
            "placeholderText": "Place holder text",
        },
        "group": {"id": parameter_group_id},
    }
    product_id = require_context_id(context, "catalog.product.id", "creating product parameter")
    return await mpt_vendor.catalog.products.parameters(product_id).create(parameter_data)


async def create_document(
    context: Context = Provide[Container.context],
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
) -> Document:
    """Creates a product document."""
    product_id = require_context_id(context, "catalog.product.id", "creating product document")
    document_data = {
        "name": "E2E Seeded",
        "description": "E2E Seeded",
        "language": "en-gb",
        "url": "",
        "documenttype": "File",
    }
    with PDF.open("rb") as pdf_fd:
        return await mpt_vendor.catalog.products.documents(product_id).create(
            document_data, file=pdf_fd
        )


async def create_item_group(
    context: Context = Provide[Container.context],
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
) -> ItemGroup:
    """Creates a product item group."""
    product_id = require_context_id(context, "catalog.product.id", "creating product item group")
    item_group_data = {
        "product": {"id": product_id},
        "name": "E2E Seeded",
        "label": "E2E Seeded",
        "description": "E2E Seeded",
        "displayOrder": 100,
        "default": False,
        "multiple": True,
        "required": True,
    }

    return await mpt_vendor.catalog.products.item_groups(product_id).create(item_group_data)


async def create_unit_of_measure(
    operations: AsyncMPTClient = Provide[Container.mpt_operations],
) -> UnitOfMeasure:
    """Creates a new unit of measure in the vendor's catalog."""
    short_uuid = uuid.uuid4().hex[:8]
    return await operations.catalog.units_of_measure.create({
        "name": f"e2e seeded {short_uuid}",
        "description": "e2e seeded",
    })


async def create_product_item(
    context: Context = Provide[Container.context],
    mpt_vendor: AsyncMPTClient = Provide[Container.mpt_vendor],
) -> Item:
    """Creates a product item."""
    short_uuid = uuid.uuid4().hex[:8]

    unit_id = require_context_id(context, "catalog.unit.id", "creating product item")
    item_group_id = require_context_id(
        context, "catalog.product.item_group.id", "creating product item"
    )
    product_id = require_context_id(context, "catalog.product.id", "creating product item")

    product_item_data = {
        "name": "e2e - please delete",
        "description": "e2e - please delete",
        "unit": {
            "id": unit_id,
        },
        "group": {
            "id": item_group_id,
        },
        "product": {
            "id": product_id,
        },
        "terms": {"model": "quantity", "period": "1m", "commitment": "1m"},
        "externalIds": {"vendor": f"e2e-delete-{short_uuid}"},
    }
    return await mpt_vendor.catalog.items.create(product_item_data)
