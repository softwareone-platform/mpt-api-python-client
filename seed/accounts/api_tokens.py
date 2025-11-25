import logging
import pathlib

from dependency_injector.wiring import inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.api_tokens import APIToken
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_VENDOR

logger = logging.getLogger(__name__)


@inject
async def get_api_token(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> APIToken | None:
    """Get API token from context or fetch from API."""
    api_token_id = context.get_string("accounts.api_token.id")
    logger.debug("Getting API token: %s", api_token_id)
    if not api_token_id:
        return None
    try:
        api_token = context.get_resource("accounts.api_token", api_token_id)
    except ValueError:
        api_token = None
    if not isinstance(api_token, APIToken):
        logger.debug("Refreshing API token: %s", api_token_id)
        api_token = await mpt_vendor.accounts.api_tokens.get(api_token_id)
        context.set_resource("accounts.api_token", api_token)
        context["accounts.api_token.id"] = api_token.id
        return api_token
    return api_token


@inject
def build_api_token_data(
    context: Context = DEFAULT_CONTEXT,
) -> dict:
    """Get API token data dictionary for creation."""
    account_id = context.get_string("accounts.account.id")
    module_id = context.get_string("accounts.module.id")
    return {
        "account": {"id": account_id},
        "name": "E2E Seeded API Token",
        "description": "This is a seeded API token for end-to-end testing.",
        "icon": "",
        "modules": [{"id": module_id}],
    }


@inject
async def init_api_token(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> APIToken:
    """Get or create API token."""
    api_token = await get_api_token()
    if api_token is None:
        logger.debug("Creating API token ...")
        api_token_data = await build_api_token_data(context)
        api_token = await mpt_vendor.accounts.api_tokens.create(api_token_data)
        context.set_resource("accounts.api_token", api_token)
        context["accounts.api_token.id"] = api_token.id
        logger.info("API token created: %s", api_token.id)
    else:
        logger.info("API token found: %s", api_token.id)
    return api_token


@inject
async def seed_api_token(
    context: Context = DEFAULT_CONTEXT,
    mpt_vendor: AsyncMPTClient = DEFAULT_MPT_VENDOR,
) -> None:
    """Seed API token."""
    logger.debug("Seeding API token ...")
    await init_api_token(context, mpt_vendor)
    logger.debug("Seeding API token completed.")
