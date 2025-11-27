import logging
import datetime as dt
from dateutil.relativedelta import relativedelta
from typing import Any

from dependency_injector.wiring import inject
from freezegun import freeze_time
from mpt_api_client.resources.commerce.agreements import Agreement
from mpt_api_client import AsyncMPTClient
from mpt_api_client.utils import get_iso_dt_str
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_OPERATIONS


logger = logging.getLogger(__name__)


@inject
async def get_agreement(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> Agreement | None:
    """Get agreement from context or fetch from API."""
    agreement_id = context.get_string("commerce.agreement.id")
    if not agreement_id:
        return None
    try:
        agreement = context.get_resource("commerce.agreement", agreement_id)
    except ValueError:
        agreement = None
    if not isinstance(agreement, Agreement):
        logger.debug("Loading agreement: %s", agreement_id)
        agreement = await mpt_operations.commerce.agreements.get(agreement_id)
        context["commerce.agreement.id"] = agreement.id
        context.set_resource("commerce.agreement", agreement)
        return agreement
    return agreement


@inject
@freeze_time("2025-11-14T09:00:00.000Z")
async def build_agreement(
    context: Context = DEFAULT_CONTEXT,
) -> dict[str, Any]:
    """Build agreement data dictionary for creation."""
    account_id = context.get_string("accounts.account.id")
    seller_id = context.get_string("accounts.seller.id")
    buyer_id = context.get_string("accounts.buyer.id")
    licensee_id = context.get_string("accounts.licensee.id")
    product_id = context.get_string("catalog.product.id")
    template_id = context.get_string("commerce.product.template.id")

    external_operations_id = "e2e-ext-ops-id-12345"
    start_date = dt.datetime.now(tz=dt.UTC)
    end_date = start_date + relativedelta(years=1)

    return {
        "name": "E2E Seeded Agreement",
        "status": "Active",
        "client": {"id": account_id},
        "seller": {"id": seller_id},
        "buyer": {"id": buyer_id},
        "licensee": {"id": licensee_id},
        "product": {"id": product_id},
        "value": {
            "PPxY": 150,
            "PPxM": 12.50,
            "SPxY": 165,
            "SPxM": 13.75,
            "markup": 0.10,
            "margin": 0.11,
            "currency": "USD"
        },
        "startDate": get_iso_dt_str(start_date),
        "endDate": get_iso_dt_str(end_date),
        "template": {"id": template_id},
        "externalIDs": {"operations":	external_operations_id}
    }


@inject
async def init_agreement(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> dict[str, Any]:
    """Get or create agreement data dictionary."""
    agreement = get_agreement()
    if agreement is None:
        logger.debug("Creating agreement data ...")
        agreement_data = build_agreement(context)
        agreement = await mpt_operations.commerce.agreements.create(agreement_data)
        logger.info("Agreement data created.")
        return agreement_data
    else:
        logger.info("Agreement found: %s", agreement.id)
        return {}


@inject
async def seed_agreement() -> None:
    """Seed agreement data."""
    logger.info("Seeding agreement data ...")
    await init_agreement()
    logger.info("Seeding agreement data completed.")
