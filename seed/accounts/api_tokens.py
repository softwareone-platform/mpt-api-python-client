import logging
import os

from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.api_tokens import ApiToken
from seed.container import Container
from seed.context import Context

logger = logging.getLogger(__name__)


@inject
async def get_api_token(
    context: Context = Provide[Container.context],
    mpt_ops: AsyncMPTClient = Provide[Container.mpt_operations],
) -> ApiToken | None:
    """Get API token from context or fetch from API."""
    api_token_id = context.get_string("accounts.api_token.id")
    if not api_token_id:
        return None
    try:
        api_token = context.get_resource("accounts.api_token", api_token_id)
    except ValueError:
        api_token = None
    if not isinstance(api_token, ApiToken):
        api_token = await mpt_ops.accounts.api_tokens.get(api_token_id)
        context.set_resource("accounts.api_token", api_token)
        context["accounts.api_token.id"] = api_token.id
        return api_token
    return api_token


@inject
def build_api_token_data(
    context: Context = Provide[Container.context],
) -> dict[str, object]:
    """Get API token data dictionary for creation."""
    account_id = os.getenv("CLIENT_ACCOUNT_ID")
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
    context: Context = Provide[Container.context],
    mpt_ops: AsyncMPTClient = Provide[Container.mpt_operations],
) -> ApiToken:
    """Get or create API token."""
    api_token = await get_api_token(context=context, mpt_ops=mpt_ops)
    if api_token is None:
        logger.debug("Creating API token ...")
        api_token_data = build_api_token_data(context=context)
        api_token = await mpt_ops.accounts.api_tokens.create(api_token_data)
        context.set_resource("accounts.api_token", api_token)
        context["accounts.api_token.id"] = api_token.id
        logger.info("API token created: %s", api_token.id)
    else:
        logger.info("API token found: %s", api_token.id)
    return api_token


@inject
async def seed_api_token() -> None:
    """Seed API token."""
    logger.debug("Seeding API token ...")
    await init_api_token()
    logger.debug("Seeding API token completed.")
