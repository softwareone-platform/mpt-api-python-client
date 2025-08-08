from typing import Any, ClassVar, Self, override

from box import Box
from httpx import Response

from mpt_api_client.models.base import BaseResource, ResourceData
from mpt_api_client.models.meta import Meta


class Resource(BaseResource):
    """Provides a resource to interact with api data using fluent interfaces."""

    _data_key: ClassVar[str] = "data"
    _safe_attributes: ClassVar[list[str]] = ["meta", "_resource_data"]

    def __init__(self, resource_data: ResourceData | None = None, meta: Meta | None = None) -> None:
        self.meta = meta
        self._resource_data = Box(resource_data or {}, camel_killer_box=True, default_box=False)

    @classmethod
    @override
    def new(cls, resource_data: ResourceData | None = None, meta: Meta | None = None) -> Self:
        return cls(resource_data, meta)

    def __getattr__(self, attribute: str) -> Box | Any:
        """Returns the resource data."""
        return self._resource_data.__getattr__(attribute)  # type: ignore[no-untyped-call]

    @override
    def __setattr__(self, attribute: str, attribute_value: Any) -> None:
        if attribute in self._safe_attributes:
            object.__setattr__(self, attribute, attribute_value)
            return

        self._resource_data.__setattr__(attribute, attribute_value)  # type: ignore[no-untyped-call]

    @classmethod
    @override
    def from_response(cls, response: Response) -> Self:
        response_data = response.json().get(cls._data_key)
        if not isinstance(response_data, dict):
            raise TypeError("Response data must be a dict.")
        meta = Meta.from_response(response)
        return cls.new(response_data, meta)

    @override
    def to_dict(self) -> dict[str, Any]:
        return self._resource_data.to_dict()
