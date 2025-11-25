# mypy: disable-error-code=unreachable
import logging
import os

from dependency_injector.wiring import inject

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.accounts.user_groups import UserGroup
from seed.context import Context
from seed.defaults import DEFAULT_CONTEXT, DEFAULT_MPT_OPERATIONS

logger = logging.getLogger(__name__)


@inject
async def get_user_group(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> UserGroup | None:
    """Get user group from context or fetch from API."""
    user_group_id = context.get_string("accounts.user_group.id")
    if not user_group_id:
        return None
    try:
        user_group = context.get_resource("accounts.user_group", user_group_id)
    except ValueError:
        user_group = None
    if not isinstance(user_group, UserGroup):
        user_group = await mpt_operations.accounts.user_groups.get(user_group_id)
        context.set_resource("accounts.user_group", user_group)
        context["accounts.user_group.id"] = user_group.id
        return user_group
    return user_group


@inject
def build_user_group_data(
    context: Context = DEFAULT_CONTEXT,
) -> dict[str, object]:
    """Get user group data dictionary for creation."""
    account_id = os.getenv("CLIENT_ACCOUNT_ID")
    if not account_id:
        raise ValueError("CLIENT_ACCOUNT_ID environment variable is required")
    module_id = context.get_string("accounts.module.id")
    return {
        "name": "E2E Seeded User Group",
        "account": {"id": account_id},
        "buyers": None,
        "logo": "",
        "description": "User group for E2E tests",
        "modules": [{"id": module_id}],
    }


@inject
async def init_user_group(
    context: Context = DEFAULT_CONTEXT,
    mpt_operations: AsyncMPTClient = DEFAULT_MPT_OPERATIONS,
) -> UserGroup | None:
    """Get or create user group."""
    user_group = await get_user_group(context=context, mpt_operations=mpt_operations)
    if user_group is not None:
        logger.info("User group already exists: %s", user_group.id)
        return user_group

    logger.debug("Creating user group ...")
    user_group_data = build_user_group_data(context=context)
    created = await mpt_operations.accounts.user_groups.create(user_group_data)
    if isinstance(created, UserGroup):
        context.set_resource("accounts.user_group", created)
        context["accounts.user_group.id"] = created.id
        logger.info("User group created: %s", created.id)
        return created

    logger.warning("User group creation failed")
    return None


@inject
async def seed_user_group() -> UserGroup | None:
    """Seed user group."""
    logger.debug("Seeding user group ...")
    user_group = await init_user_group()
    logger.debug("Seeding user group completed.")
    return user_group
