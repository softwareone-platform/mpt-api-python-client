import logging
import pathlib

from dependency_injector.wiring import Provide, inject

from seed.accounts.accounts import seed_accounts
from seed.catalog.catalog import seed_catalog
from seed.container import Container
from seed.context import Context, load_context, save_context

logger = logging.getLogger(__name__)

context_file: pathlib.Path = pathlib.Path(__file__).parent / "context.json"


@inject
async def seed_api(context: Context = Provide[Container.context]) -> None:
    """Seed API."""
    load_context(context_file, context)
    try:  # noqa: WPS229
        await seed_accounts()
        await seed_catalog()
        logger.info("Seeding completed successfully.")
    except Exception:
        logger.exception("Exception occurred during seeding.")
    finally:
        save_context(context, context_file)
