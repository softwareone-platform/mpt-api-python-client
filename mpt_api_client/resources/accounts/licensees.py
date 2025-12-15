from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateFileMixin,
    AsyncDeleteMixin,
    AsyncDisableMixin,
    AsyncEnableMixin,
    AsyncGetMixin,
    AsyncUpdateFileMixin,
    CollectionMixin,
    CreateFileMixin,
    DeleteMixin,
    DisableMixin,
    EnableMixin,
    GetMixin,
    UpdateFileMixin,
)
from mpt_api_client.models import Model


class Licensee(Model):
    """Licensee Model."""


class LicenseesServiceConfig:
    """Licensees Service Configuration."""

    _endpoint = "/public/v1/accounts/licensees"
    _model_class = Licensee
    _collection_key = "data"
    _upload_file_key = "logo"
    _upload_data_key = "licensee"


class LicenseesService(
    CreateFileMixin[Licensee],
    UpdateFileMixin[Licensee],
    EnableMixin[Licensee],
    DisableMixin[Licensee],
    GetMixin[Licensee],
    DeleteMixin,
    CollectionMixin[Licensee],
    Service[Licensee],
    LicenseesServiceConfig,
):
    """Licensees Service."""


class AsyncLicenseesService(
    AsyncCreateFileMixin[Licensee],
    AsyncUpdateFileMixin[Licensee],
    AsyncEnableMixin[Licensee],
    AsyncDisableMixin[Licensee],
    AsyncGetMixin[Licensee],
    AsyncDeleteMixin,
    AsyncCollectionMixin[Licensee],
    AsyncService[Licensee],
    LicenseesServiceConfig,
):
    """Async Licensees Service."""
