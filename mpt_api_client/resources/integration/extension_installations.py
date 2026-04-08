from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncGetMixin,
    CollectionMixin,
    GetMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class ExtensionInstallation(Model):
    """Extension Installation resource.

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
        audit: Audit information.
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


class ExtensionInstallationsServiceConfig:
    """Extension Installations service configuration."""

    _endpoint = "/public/v1/integration/extensions/{extension_id}/installations"
    _model_class = ExtensionInstallation
    _collection_key = "data"


class ExtensionInstallationsService(
    GetMixin[ExtensionInstallation],
    CollectionMixin[ExtensionInstallation],
    Service[ExtensionInstallation],
    ExtensionInstallationsServiceConfig,
):
    """Sync service for /public/v1/integration/extensions/{extensionId}/installations endpoint."""


class AsyncExtensionInstallationsService(
    AsyncGetMixin[ExtensionInstallation],
    AsyncCollectionMixin[ExtensionInstallation],
    AsyncService[ExtensionInstallation],
    ExtensionInstallationsServiceConfig,
):
    """Async service for /public/v1/integration/extensions/{extensionId}/installations endpoint."""
