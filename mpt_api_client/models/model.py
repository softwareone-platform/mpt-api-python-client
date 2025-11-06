from typing import Any, ClassVar, Self, override

from box import Box

from mpt_api_client.http.types import Response
from mpt_api_client.models.meta import Meta

ResourceData = dict[str, Any]


class Model:  # noqa: WPS214
    """Provides a resource to interact with api data using fluent interfaces."""

    _data_key: ClassVar[str | None] = None
    _safe_attributes: ClassVar[list[str]] = ["meta", "_box"]

    def __init__(self, resource_data: ResourceData | None = None, meta: Meta | None = None) -> None:
        self.meta = meta
        self._box = Box(resource_data or {}, camel_killer_box=False, default_box=False)

    @classmethod
    def new(cls, resource_data: ResourceData | None = None, meta: Meta | None = None) -> Self:
        """Creates a new resource from ResourceData and Meta."""
        return cls(resource_data, meta)

    def __getattr__(self, attribute: str) -> Box | Any:
        """Returns the resource data."""
        return self._box.__getattr__(attribute)  # type: ignore[no-untyped-call]

    @override
    def __setattr__(self, attribute: str, attribute_value: Any) -> None:
        if attribute in self._safe_attributes:
            object.__setattr__(self, attribute, attribute_value)
            return

        self._box.__setattr__(attribute, attribute_value)  # type: ignore[no-untyped-call]

    @classmethod
    def from_response(cls, response: Response) -> Self:
        """Creates a collection from a response.

        Args:
            response: The httpx response object.
        """
        response_data = response.json()
        if isinstance(response_data, dict):
            response_data.pop("$meta", None)
        if cls._data_key:
            response_data = response_data.get(cls._data_key)
        if not isinstance(response_data, dict):
            raise TypeError("Response data must be a dict.")
        meta = Meta.from_response(response)
        return cls.new(response_data, meta)

    @property
    def id(self) -> str:
        """Returns the resource ID."""
        return str(self._box.get("id", ""))  # type: ignore[no-untyped-call]

    def to_dict(self) -> dict[str, Any]:
        """Returns the resource as a dictionary."""
        return self._box.to_dict()

    @override
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}>"  # noqa: WPS237
