from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.integration.mixins import (
    AsyncInstallationMixin,
    InstallationMixin,
)


class Installation(Model):
    """Installation resource.

    Attributes:
        name: Installation name.
        revision: Revision number.
        account: Reference to the account.
        extension: Reference to the extension.
        status: Installation status (Invited, Installed, Uninstalled, Expired).
        configuration: Installation configuration data.
        invitation: Invitation details.
        modules: Modules included in the installation.
        terms: Accepted terms for this installation.
        audit: Audit information (created, updated, invited, installed, expired, uninstalled).
    """

    name: str | None
    revision: int | None
    account: BaseModel | None
    extension: BaseModel | None
    status: str | None
    configuration: BaseModel | None
    invitation: BaseModel | None
    modules: list[BaseModel] | None
    terms: list[BaseModel] | None
    audit: BaseModel | None


class InstallationsServiceConfig:
    """Installations service configuration."""

    _endpoint = "/public/v1/integration/installations"
    _model_class = Installation
    _collection_key = "data"


class InstallationsService(
    InstallationMixin[Installation],
    ManagedResourceMixin[Installation],
    CollectionMixin[Installation],
    Service[Installation],
    InstallationsServiceConfig,
):
    """Sync service for the /public/v1/integration/installations endpoint."""


class AsyncInstallationsService(
    AsyncInstallationMixin[Installation],
    AsyncManagedResourceMixin[Installation],
    AsyncCollectionMixin[Installation],
    AsyncService[Installation],
    InstallationsServiceConfig,
):
    """Async service for the /public/v1/integration/installations endpoint."""
