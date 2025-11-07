from typing import Any, ClassVar, Self, override

from box import Box
from box.box import _camel_killer  # type: ignore[attr-defined] # noqa: PLC2701

from mpt_api_client.http.types import Response
from mpt_api_client.models.meta import Meta

ResourceData = dict[str, Any]


class MptBox(Box):
    """python-box that preserves camelCase keys when converted to json."""

    def __init__(self, *args, key_mapping: dict[str, str] | None, **kwargs):  # type: ignore[no-untyped-def]
        super().__init__(*args, **kwargs)
        key_mapping = key_mapping or {}
        if self._box_config.get("key_mapping") is None:
            self._box_config["key_mapping"] = key_mapping
        else:
            self._box_config.get("key_mapping").update(key_mapping)

    @override
    def __setitem__(self, key, value):  # type: ignore[no-untyped-def]  # noqa: WPS110
        try:
            mapped_key = self._box_config["key_mapping"][key]
        except KeyError as error:
            if key == "key_mapping" and "key_mapping" in self._box_config:
                return
            if error.args[0] == "key_mapping" and "key_mapping" not in self._box_config:
                self._box_config["key_mapping"] = self._box_config.get("default_key_mappings", {})

            mapped_key = _camel_killer(key)
            self._box_config["key_mapping"][key] = mapped_key
        super().__setitem__(mapped_key, value)  # type: ignore[no-untyped-call]

    @override
    def to_dict(self) -> dict[str, Any]:  # noqa: WPS210
        reverse_mapping = {
            mapped_key: original_key
            for original_key, mapped_key in self._box_config.get("key_mapping", {}).items()
        }
        out_dict = {}
        for parsed_key, item_value in super().to_dict().items():
            original_key = reverse_mapping[parsed_key]
            out_dict[original_key] = item_value
        return out_dict


class Model:  # noqa: WPS214
    """Provides a resource to interact with api data using fluent interfaces."""

    _data_key: ClassVar[str | None] = None
    _safe_attributes: ClassVar[list[str]] = ["meta", "_box"]
    _case_mappings: ClassVar[dict[str, str]] = {}

    def __init__(self, resource_data: ResourceData | None = None, meta: Meta | None = None) -> None:
        self.meta = meta
        self._box = MptBox(
            resource_data or {},
            camel_killer_box=False,
            default_box=False,
            default_box_create_on_get=False,
            key_mapping=self._case_mappings,
        )

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
