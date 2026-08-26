from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Self

from mpt_api_client.constants import MPT_META_DELETED_FIELD, MPT_META_FIELD

RECORD_ID_FIELD = "id"


def is_deletion_stub(record: Mapping[str, Any]) -> bool:
    """Report whether a streamed record is a deletion stub rather than data.

    ``$meta.deleted`` is the platform's metadata channel for the signal and is absent from
    a normal record. A truthy ``deleted`` marker is what identifies a stub, so a record
    carrying no ``$meta``, no ``deleted`` key, or a falsy one is data rather than a deletion.

    Args:
        record: Deserialized record read from one line of a stream.

    Returns:
        True when the record carries a truthy ``$meta.deleted`` marker.
    """
    record_meta = record.get(MPT_META_FIELD)
    if not isinstance(record_meta, Mapping):
        return False
    return bool(record_meta.get(MPT_META_DELETED_FIELD))


@dataclass(frozen=True)
class DeletionStub:
    """Identifies a row deleted after the membership snapshot a stream was opened on.

    The platform emits one of these in place of a record whose row was hard-deleted after
    the export's membership snapshot, marking it with ``$meta.deleted`` and guaranteeing
    only its ``id``. It is deliberately not a `Model`: a stub carries no record data, so
    deserializing it as one would produce an instance whose every field is None, and a
    caller writing that back would overwrite the stored record with nulls.

    It is also distinct from the domain ``DELETED`` status, which is a state of a full
    record that still exists. A stub marks a row that no longer exists at all.
    """

    id: str

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> Self:
        """Build a stub from a record `is_deletion_stub` accepted.

        Args:
            record: Deserialized record marked with ``$meta.deleted``.

        Returns:
            The stub identifying the deleted row.

        Raises:
            TypeError: If the record carries no string ``id``, the one property the
                contract guarantees on a stub.
        """
        record_id = record.get(RECORD_ID_FIELD)
        if not isinstance(record_id, str):
            raise TypeError("A deletion stub must carry a string 'id'.")
        return cls(id=record_id)
