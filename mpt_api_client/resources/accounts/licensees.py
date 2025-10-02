from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncUpdateMixin,
    CreateMixin,
    DeleteMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.accounts.mixins import AsyncEnablableMixin, EnablableMixin


class Licensee(Model):
    """Licensee Model."""


class LicenseesServiceConfig:
    """Licensees Service Configuration."""

    _endpoint = "/public/v1/accounts/licensees"
    _model_class = Licensee
    _collection_key = "data"


class LicenseesService(
    CreateMixin[Licensee],
    DeleteMixin,
    UpdateMixin[Licensee],
    EnablableMixin[Licensee],
    Service[Licensee],
    LicenseesServiceConfig,
):
    """Licensees Service."""


class AsyncLicenseesService(
    AsyncCreateMixin[Licensee],
    AsyncDeleteMixin,
    AsyncUpdateMixin[Licensee],
    AsyncEnablableMixin[Licensee],
    AsyncService[Licensee],
    LicenseesServiceConfig,
):
    """Async Licensees Service."""
