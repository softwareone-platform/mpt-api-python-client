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
    """
    Retrieve the ApiToken from context if present; otherwise fetch it from the API and store it in context.
    
    If the token is fetched, it is saved in the context resources under "accounts.api_token" and "accounts.api_token.id" is updated.
    
    Returns:
        `ApiToken` if found or fetched, `None` if no token id is present in context.
    """
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
    """
    Builds the dictionary of fields required to create an API token used for end-to-end testing.
    
    The returned mapping includes:
    - `account`: `{"id": <CLIENT_ACCOUNT_ID environment variable>}`
    - `name`: token display name
    - `description`: token description
    - `icon`: token icon (empty string when not set)
    - `modules`: list containing a module object with `id` read from the context key "accounts.module.id"
    
    Returns:
        dict[str, object]: The payload suitable for API token creation.
    """
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
    """
    Ensure an API token exists for the account, creating and persisting one if necessary.
    
    If an API token is not already available, creates a new token and stores it in the context resource "accounts.api_token" and updates "accounts.api_token.id".
    
    Returns:
        ApiToken: The existing or newly created API token instance.
    """
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