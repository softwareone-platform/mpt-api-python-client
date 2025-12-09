import logging

from dependency_injector.wiring import Provide, inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.api_tokens import ApiToken
from seed.container import Container
from seed.context import Context
from seed.helper import init_resource, require_context_id

logger = logging.getLogger(__name__)


@inject
def build_api_token_data(
    context: Context = Provide[Container.context],
) -> dict[str, object]:
    """Get API token data dictionary for creation."""
    account_id = require_context_id(context, "accounts.client_account.id", "creating API token")
    module_id = require_context_id(context, "accounts.module.id", "creating API token")
    return {
        "account": {"id": account_id},
        "name": "E2E Seeded API Token",
        "description": "This is a seeded API token for end-to-end testing.",
        "icon": "",
        "modules": [{"id": module_id}],
    }


@inject
async def create_api_token(
    context: Context = Provide[Container.context],
    mpt_ops: AsyncMPTClient = Provide[Container.mpt_operations],
) -> ApiToken:
    """Creates an API token."""
    logger.debug("Creating API token ...")
    api_token_data = build_api_token_data(context=context)
    return await mpt_ops.accounts.api_tokens.create(api_token_data)


async def seed_api_token() -> None:
    """Seed API token."""
    logger.debug("Seeding API token ...")
    await init_resource("accounts.api_token.id", create_api_token)
    logger.debug("Seeding API token completed.")
