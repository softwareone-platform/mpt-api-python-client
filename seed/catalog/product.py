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
    result: Product | None = None
    if product_id:
        try:
            maybe = context.get_resource(namespace, product_id)
        except ValueError:
            maybe = None
        if isinstance(maybe, Product):
            result = maybe
        else:
            logger.debug("Refreshing product: %s", product_id)
            refreshed = await mpt_vendor.catalog.products.get(product_id)
            if isinstance(refreshed, Product):
                context.set_resource(namespace, refreshed)
                context[f"{namespace}.id"] = refreshed.id
                result = refreshed
    return result


@inject
async def init_product(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> Product:
    """Get or create product."""
    product = await get_product()
    if product is not None:
        logger.info("Product found: %s", product.id)
        return product
    logger.debug("Creating product ...")
    with pathlib.Path.open(icon, "rb") as icon_file:
        created = await mpt_vendor.catalog.products.create(
            {"name": "E2E Seeded", "website": "https://www.example.com"}, file=icon_file
        )
    if isinstance(created, Product):
        context.set_resource(namespace, created)
        context[f"{namespace}.id"] = created.id
        logger.info("Product created: %s", created.id)
        return created
    logger.warning("Product creation failed")
    raise ValueError("Product creation failed")


@inject
async def review_product(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> Product | None:
    """Review product if in draft status."""
    product = await get_product()
    if not isinstance(product, Product) or product.status != "Draft":
        return product
    logger.debug("Reviewing product: %s", product.id)
    reviewed = await mpt_vendor.catalog.products.review(product.id)
    if isinstance(reviewed, Product):
        context.set_resource(namespace, reviewed)
        return reviewed
    logger.warning("Product review failed")
    return None


@inject
async def publish_product(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> Product | None:
    """Publish product if in reviewing status."""
    product = await get_product()
    if not isinstance(product, Product) or product.status != "Reviewing":
        return product
    logger.debug("Publishing product: %s", product.id)
    published = await mpt_operations.catalog.products.publish(product.id)
    if isinstance(published, Product):
        context.set_resource(namespace, published)
        return published
    logger.warning("Product publish failed")
    return None


async def seed_product() -> None:
    """Seed product data."""
    logger.debug("Seeding catalog.product ...")
    await init_product()
    await review_product()
    await publish_product()
    logger.debug("Seeded catalog.product completed.")
