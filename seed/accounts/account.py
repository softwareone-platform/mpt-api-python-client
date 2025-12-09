import logging
import os
from functools import partial

from dependency_injector.wiring import Provide, inject

from seed.container import Container
from seed.context import Context
from seed.helper import init_resource

logger = logging.getLogger(__name__)


@inject
async def init_account_id(env_var: str, context: Context = Provide[Container.context]) -> str:  # noqa: RUF029
    """Generic initializer for account IDs from environment variables."""
    account_id = os.getenv(env_var)
    if not account_id:
        raise ValueError(f"{env_var} environment variable is required")
    return account_id


async def seed_account_ids() -> None:
    """Seed account."""
    logger.debug("Seeding vendor account ...")
    await init_resource(
        "accounts.account.id",
        partial(init_account_id, "VENDOR_ACCOUNT_ID", context=Provide[Container.context]),
    )
    await init_resource(
        "accounts.client_account.id",
        partial(init_account_id, "CLIENT_ACCOUNT_ID", context=Provide[Container.context]),
    )
    await init_resource(
        "accounts.operations_account.id",
        partial(init_account_id, "OPERATIONS_ACCOUNT_ID", context=Provide[Container.context]),
    )
    logger.debug("Seeding account completed.")
