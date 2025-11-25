import logging
import pathlib

from dependency_injector.wiring import inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.accounts import Accounts
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_VENDOR

icon = pathlib.Path(__file__).parent / "logo.png"

logger = logging.getLogger(__name__)

namespace = "accounts.account"

@inject
async def get_account(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> Accounts:
    """Get account from context or fetch from API."""
    account_id = context.get_string(f"{namespace}.id")
    logger.debug("Getting account: %s", account_id)
    if not account_id:
        return None
    try:
        account = context.get_resource(namespace, account_id)
    except ValueError:
        account = None
    if not isinstance(account, Accounts):
        logger.debug("Refreshing account: %s", account_id)
        account = await mpt_vendor.accounts.accounts.get(account_id)
        context.set_resource(namespace, account)
        context[f"{namespace}.id"] = account.id
        return account
    return account


@inject
async def init_account(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> Accounts:
    """Get or create account."""
    account = await get_account()
    if account is None:
        logger.debug("Creating account ...")
        with pathlib.Path.open(icon, "rb") as icon_file:
            account_data = {
                    "name": "E2E Seeded Account",
                    "address": {
                        "addressLine1": "123 Test St",
                        "city": "San Francisco",
                        "state": "CA",
                        "postCode": "12345",
                        "country": "US",
                    },
                    "type": "Vendor",
                    "status": "Active",
                }
            account = await mpt_vendor.accounts.accounts.create(
                account_data, file=icon_file
            )
            context.set_resource(namespace, account)
            context[f"{namespace}.id"] = account.id
        logger.info("Account created: %s", account.id)
    else:
        logger.info("Account found: %s", account.id)
    return account


async def seed_account() -> None:
    """Seed account data."""
    logger.debug("Seeding account ...")
    await init_account()
    logger.info("Account seeded.")
