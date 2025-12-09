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
    """
    Initialize and seed application data using the provided Context.
    
    Loads the persisted context from the module's context file, seeds accounts and then catalog data, logs any exception raised during seeding, and always saves the updated context back to the context file.
    
    Parameters:
        context (Context): Context object used for seeding; provided by the dependency injection container by default.
    """
    load_context(context_file, context)
    try:  # noqa: WPS229
        await seed_accounts()
        await seed_catalog()
    except Exception:
        logger.exception("Exception occurred during seeding.")
    finally:
        save_context(context, context_file)