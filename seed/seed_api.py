import asyncio
import logging
import pathlib

from dependency_injector.wiring import inject

from seed.accounts.accounts import seed_accounts
from seed.catalog.catalog import seed_catalog
from seed.context import Context, load_context, save_context
from seed.defaults import DEFAULT_CONTEXT

logger = logging.getLogger(__name__)

context_file: pathlib.Path = pathlib.Path(__file__).parent / "context.json"


@inject
async def seed_api(context: Context = DEFAULT_CONTEXT) -> None:
    """Seed API."""
    tasks = []

    load_context(context_file, context)

    tasks.extend((
        asyncio.create_task(seed_catalog()),
        asyncio.create_task(seed_accounts())
    ))

    try:
        await asyncio.gather(*tasks)
    except Exception:
        logger.exception("Exception occurred during seeding.")
    finally:
        save_context(context, context_file)
