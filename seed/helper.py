import logging
from collections.abc import Awaitable, Callable
from typing import Any

from dependency_injector.wiring import Provide

from seed.container import Container
from seed.context import Context

logger = logging.getLogger(__name__)


class ResourceRequiredError(Exception):
    """Raised when a resource is required but not found."""

    def __init__(self, context: Context, key: str, action: str):
        super().__init__(f"Missing required resource '{key}' before {action}.")
        self.context = context
        self.key = key
        self.action = action


def require_context_id(context: Context, key: str, action: str) -> str:
    """Fetch an ID from context, ensuring it exists and is non-empty.

    Args:
        context: The seeding context.
        key: The expected context key where the id is stored.
        action: A short description of what we are creating (for error message).

    Returns:
        The id string stored in the context under the provided key.

    Raises:
        ResourceRequiredError: If the id is missing or empty in context.
    """
    resource_id = context.get_string(key)
    if not resource_id:
        raise ResourceRequiredError(context, key, action)
    return resource_id


async def init_resource(
    namespace: str,
    resource_factory: Callable[[], Awaitable[Any]],
    context: Context = Provide[Container.context],
) -> str:
    """Initialize a resource on demand and cache its id in the Context.

    This helper reads an id from the provided Context at the given namespace. If the id
    is missing or empty, it will call the provided async ``resource_factory`` to create
    the resource, extract the ``id`` from the returned object, store it back into the
    Context under ``namespace``, and return it. If the id already exists in the Context,
    the factory is not called and the existing id is returned.

    Args:
        namespace: The Context key where the resource id is stored (e.g.,
            "catalog.product.id").
        resource_factory: A zero-argument async callable that creates the resource when
            needed. It must return an object with an ``id`` attribute (string-like).
        context: The seeding Context used to read and persist the id. Defaults to
            ``DEFAULT_CONTEXT``.

    Returns:
        The resource id string, either retrieved from the Context or obtained from the
            newly created resource.

    Notes:
        - The factory is invoked only if the id is not already present in the Context.
        - Any exceptions thrown by ``resource_factory`` will propagate to the caller.
        - No additional validation of the returned id is performed beyond attribute access.

    Example:
        In an async function/context you can do:
        id_value = await init_resource("catalog.product.id", create_product, context)
    """
    logger.debug("Initializing resource: %s", namespace)
    id_value = context.get_string(namespace)
    if not id_value:
        resource = await resource_factory()
        id_value = resource.id
        context[namespace] = id_value
    return id_value
