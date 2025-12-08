from dependency_injector import containers, providers

from mpt_api_client import AsyncMPTClient
from seed.context import Context


class Container(containers.DeclarativeContainer):
    """Dependency injection container for MPT clients."""

    config = providers.Configuration()

    # Client factories
    mpt_client = providers.Factory(
        AsyncMPTClient.from_config,
        api_token=config.mpt_api_token_client,
        base_url=config.mpt_api_base_url,
    )

    mpt_vendor = providers.Factory(
        AsyncMPTClient.from_config,
        api_token=config.mpt_api_token_vendor,
        base_url=config.mpt_api_base_url,
    )

    mpt_operations = providers.Factory(
        AsyncMPTClient.from_config,
        api_token=config.mpt_api_token_operations,
        base_url=config.mpt_api_base_url,
    )

    # Context provider - stores application context as a singleton
    context: providers.Singleton[Context] = providers.Singleton(Context)


# Create container instance
container = Container()

# Configure from environment variables
container.config.mpt_api_base_url.from_env("MPT_API_BASE_URL")
container.config.mpt_api_token_client.from_env("MPT_API_TOKEN_CLIENT")
container.config.mpt_api_token_vendor.from_env("MPT_API_TOKEN_VENDOR")
container.config.mpt_api_token_operations.from_env("MPT_API_TOKEN_OPERATIONS")


def wire_container() -> None:
    """Wire the dependency injection container."""
    container.wire(packages=["seed"])
