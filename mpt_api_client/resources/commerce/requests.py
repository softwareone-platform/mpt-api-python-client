from mpt_api_client.http import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncService,
    AsyncUpdateMixin,
    CreateMixin,
    DeleteMixin,
    Service,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.commerce.mixins import (
    AsyncCompleteMixin,
    AsyncProcessMixin,
    AsyncQueryMixin,
    AsyncTemplateMixin,
    AsyncValidateMixin,
    CompleteMixin,
    ProcessMixin,
    QueryMixin,
    TemplateMixin,
    ValidateMixin,
)


class Request(Model):
    """Request model."""


class RequestServiceConfig:
    """Request service config."""

    _endpoint = "/public/v1/commerce/orders"
    _model_class = Request
    _collection_key = "data"


class RequestService(
    CreateMixin[Request],
    UpdateMixin[Request],
    DeleteMixin,
    ValidateMixin[Request],
    ProcessMixin[Request],
    QueryMixin[Request],
    CompleteMixin[Request],
    TemplateMixin,
    Service[Request],
    RequestServiceConfig,
):
    """Request service model."""


class AsyncRequestService(
    AsyncCreateMixin[Request],
    AsyncUpdateMixin[Request],
    AsyncDeleteMixin,
    AsyncValidateMixin[Request],
    AsyncProcessMixin[Request],
    AsyncQueryMixin[Request],
    AsyncCompleteMixin[Request],
    AsyncTemplateMixin,
    AsyncService[Request],
    RequestServiceConfig,
):
    """Async Request service model."""
