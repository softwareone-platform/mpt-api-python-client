import logging

from seed.accounts.account import seed_account_ids
from seed.accounts.api_tokens import seed_api_token
from seed.accounts.buyer import seed_buyer
from seed.accounts.licensee import seed_licensee
from seed.accounts.module import seed_module
from seed.accounts.seller import seed_seller
from seed.accounts.user_group import seed_user_group

logger = logging.getLogger(__name__)


async def seed_accounts() -> None:  # noqa: WPS217, WPS213
    """Seed accounts data including account."""
    logger.debug("Seeding accounts ...")

    await seed_account_ids()

    await seed_seller()
    await seed_buyer()
    await seed_module()
    await seed_api_token()
    await seed_user_group()
    await seed_licensee()

    logger.debug("Seeded accounts completed.")
