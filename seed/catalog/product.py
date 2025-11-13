import logging
import pathlib

from dependency_injector.wiring import inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.catalog.products import Product
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_OPERATIONS, DEFAULT_MPT_VENDOR

icon = pathlib.Path(__file__).parent / "FIL-9920-4780-9379.png"

logger = logging.getLogger(__name__)

namespace = "catalog.product"


@inject
async def get_product(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> Product | None:
    """Get product from context or fetch from API."""
    product_id = context.get_string(f"{namespace}.id")
    logger.debug("Getting product: %s", product_id)
    if not product_id:
        return None
    try:
        product = context.get_resource(namespace, product_id)
    except ValueError:
        product = None
    if not isinstance(product, Product):
        logger.debug("Refreshing product: %s", product_id)
        product = await mpt_vendor.catalog.products.get(product_id)
        context.set_resource(namespace, product)
        context[f"{namespace}.id"] = product.id
        return product
    return product


@inject
async def init_product(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> Product:
    """Get or create product."""
    product = await get_product()
    if product is None:
        logger.debug("Creating product ...")
        with pathlib.Path.open(icon, "rb") as icon_file:
            product = await mpt_vendor.catalog.products.create(
                {"name": "E2E Seeded", "website": "https://www.example.com"}, icon=icon_file
            )
            context.set_resource(namespace, product)
            context[f"{namespace}.id"] = product.id
        logger.info("Product created: %s", product.id)
    else:
        logger.info("Product found: %s", product.id)
    return product


@inject
async def review_product(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> Product | None:
    """Review product if in draft status."""
    product = await get_product()
    if not product or product.status != "Draft":
        return product
    logger.debug("Reviewing product: %s", product.id)
    product = await mpt_vendor.catalog.products.review(product.id)
    context.set_resource(namespace, product)
    return product


@inject
async def publish_product(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> Product | None:
    """Publish product if in reviewing status."""
    product = await get_product()
    if not product or product.status != "Reviewing":
        return product
    logger.debug("Publishing product: %s", product.id)
    product = await mpt_operations.catalog.products.publish(product.id)
    context.set_resource(namespace, product)
    return product


async def seed_product() -> None:
    """Seed product data."""
    logger.debug("Seeding catalog.product ...")
    await init_product()
    await review_product()
    await publish_product()
    logger.debug("Seeded catalog.product completed.")
