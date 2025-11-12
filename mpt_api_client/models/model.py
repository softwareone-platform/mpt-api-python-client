from typing import Any, ClassVar, Self, override

from box import Box
from box.box import _camel_killer  # type: ignore[attr-defined] # noqa: PLC2701

from mpt_api_client.http.types import Response
from mpt_api_client.models.meta import Meta

ResourceData = dict[str, Any]

_box_safe_attributes: list[str] = ["_box_config", "_attribute_mapping"]


class MptBox(Box):
    """python-box that preserves camelCase keys when converted to json."""

    def __init__(self, *args, attribute_mapping: dict[str, str] | None = None, **_):  # type: ignore[no-untyped-def]
        attribute_mapping = attribute_mapping or {}
        self._attribute_mapping = attribute_mapping
        super().__init__(
            *args,
            camel_killer_box=False,
            default_box=False,
            default_box_create_on_get=False,
        )

    @override
    def __setitem__(self, key, value):  # type: ignore[no-untyped-def]
        mapped_key = self._prep_key(key)
        super().__setitem__(mapped_key, value)  # type: ignore[no-untyped-call]

    @override
    def __setattr__(self, item: str, value: Any) -> None:
        if item in _box_safe_attributes:
            return object.__setattr__(self, item, value)

        super().__setattr__(item, value)  # type: ignore[no-untyped-call]
        return None

    @override
    def __getattr__(self, item: str) -> Any:
        if item in _box_safe_attributes:
            return object.__getattribute__(self, item)
        return super().__getattr__(item)  # type: ignore[no-untyped-call]

    @override
    def to_dict(self) -> dict[str, Any]:  # noqa: WPS210
        reverse_mapping = {
            mapped_key: original_key for original_key, mapped_key in self._attribute_mapping.items()
        }
        out_dict = {}
        for parsed_key, item_value in super().to_dict().items():
            original_key = reverse_mapping[parsed_key]
            out_dict[original_key] = item_value
        return out_dict

    def _prep_key(self, key: str) -> str:
        try:
            return self._attribute_mapping[key]
        except KeyError:
            self._attribute_mapping[key] = _camel_killer(key)
            return self._attribute_mapping[key]


class Model:  # noqa: WPS214
    """Provides a resource to interact with api data using fluent interfaces."""

    _data_key: ClassVar[str | None] = None
    _safe_attributes: ClassVar[list[str]] = ["meta", "_box"]
    _attribute_mapping: ClassVar[dict[str, str]] = {}

    def __init__(self, resource_data: ResourceData | None = None, meta: Meta | None = None) -> None:
        self.meta = meta
        self._box = MptBox(
            resource_data or {},
            attribute_mapping=self._attribute_mapping,
        )

    @override
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"<{class_name} {self.id}>"

    @classmethod
    def new(cls, resource_data: ResourceData | None = None, meta: Meta | None = None) -> Self:
        """Creates a new resource from ResourceData and Meta."""
        return cls(resource_data, meta)

    def __getattr__(self, attribute: str) -> Box | Any:
        """Returns the resource data."""
        return self._box.__getattr__(attribute)

    @override
    def __setattr__(self, attribute: str, attribute_value: Any) -> None:
        if attribute in self._safe_attributes:
            object.__setattr__(self, attribute, attribute_value)
            return

        self._box.__setattr__(attribute, attribute_value)

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
