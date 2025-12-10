import logging
import os

from mpt_api_client.resources.accounts.account import Account
from seed.accounts.api_tokens import seed_api_token
from seed.accounts.buyer import seed_buyer
from seed.accounts.licensee import seed_licensee
from seed.accounts.module import seed_module
from seed.accounts.seller import seed_seller
from seed.accounts.user_group import seed_user_group
from seed.helper import init_resource

logger = logging.getLogger(__name__)


async def get_account() -> Account:  # noqa: RUF029 async for compatibility purposes with init_resource
    """Get account ID from environment variable."""
    account_id = os.getenv("CLIENT_ACCOUNT_ID")
    if not account_id:
        raise ValueError("CLIENT_ACCOUNT_ID environment variable is required")
    return Account({"id": account_id})


async def seed_accounts() -> None:  # noqa: WPS213 WPS217
    """Seed accounts data including account."""
    logger.debug("Seeding accounts ...")
    await init_resource("accounts.account.id", get_account)

    await seed_seller()
    await seed_buyer()
    await seed_module()
    await seed_api_token()
    await seed_user_group()
    await seed_licensee()

    logger.debug("Seeded accounts completed.")
