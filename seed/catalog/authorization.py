import uuid

from dependency_injector.wiring import Provide

from mpt_api_client import AsyncMPTClient
from mpt_api_client.resources.catalog.authorizations import Authorization
from seed.container import Container
from seed.context import Context
from seed.helper import init_resource, require_context_id


async def seed_authorization() -> None:
    """
    Ensure the catalog authorization resource is seeded.
    
    Creates the authorization resource if it does not exist and stores its identifier under the context key "catalog.authorization.id".
    """
    await init_resource("catalog.authorization.id", create_authorization)


async def create_authorization(
    operations: AsyncMPTClient = Provide[Container.mpt_operations],
    context: Context = Provide[Container.context],
) -> Authorization:
    """
    Create an authorization in the catalog using required IDs from the provided context.
    
    Returns:
        Authorization: The created Authorization object returned by the catalog service.
    """
    product_id = require_context_id(context, "catalog.product.id", "Create authorization")
    seller_id = require_context_id(context, "accounts.seller.id", "Create authorization")
    account_id = require_context_id(context, "accounts.account.id", "Create authorization")
    short_uuid = uuid.uuid4().hex[:8]

    authorization_data = {
        "externalIds": {"operations": f"e2e-seeded-{short_uuid}"},
        "product": {"id": product_id},
        "owner": {"id": seller_id},
        "journal": {"firstInvoiceDate": "2025-12-01", "frequency": "1m"},
        "eligibility": {"client": True, "partner": True},
        "currency": "USD",
        "notes": "E2E Seeded",
        "name": "E2E Seeded",
        "vendor": {"id": account_id},
    }
    return await operations.catalog.authorizations.create(authorization_data)