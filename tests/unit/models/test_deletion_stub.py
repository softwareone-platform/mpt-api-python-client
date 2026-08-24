import dataclasses

import pytest

from mpt_api_client.models import DeletionStub, Model, is_deletion_stub

NON_STUB_RECORDS = (
    pytest.param({"id": "ID-1"}, id="no $meta at all"),
    pytest.param({"id": "ID-1", "$meta": {}}, id="$meta without the deleted marker"),
    pytest.param({"id": "ID-1", "$meta": {"deleted": False}}, id="marker explicitly false"),
    pytest.param({"id": "ID-1", "$meta": {"deleted": None}}, id="marker is null"),
    pytest.param({"id": "ID-1", "$meta": "deleted"}, id="$meta is not a mapping"),
    pytest.param({"id": "ID-1", "status": "DELETED"}, id="domain DELETED status"),
)


@pytest.fixture
def stub_record():
    return {"id": "ID-1", "$meta": {"deleted": True}}


def test_is_deletion_stub_detects_the_marker(stub_record):
    result = is_deletion_stub(stub_record)

    assert result is True


@pytest.mark.parametrize("record", NON_STUB_RECORDS)
def test_is_deletion_stub_rejects_unmarked(record):
    result = is_deletion_stub(record)

    assert result is False


def test_from_record_reads_the_id(stub_record):
    result = DeletionStub.from_record(stub_record)

    assert result == DeletionStub(id="ID-1")


@pytest.mark.parametrize(
    "record",
    [
        pytest.param({"$meta": {"deleted": True}}, id="no id at all"),
        pytest.param({"id": None, "$meta": {"deleted": True}}, id="null id"),
        pytest.param({"id": 42, "$meta": {"deleted": True}}, id="non-string id"),
    ],
)
def test_from_record_requires_a_string_id(record):
    with pytest.raises(TypeError, match="must carry a string 'id'"):
        DeletionStub.from_record(record)


def test_stub_is_not_a_model():
    result = DeletionStub(id="ID-1")

    assert not isinstance(result, Model)


def test_stub_is_immutable():
    stub = DeletionStub(id="ID-1")

    with pytest.raises(dataclasses.FrozenInstanceError):
        stub.id = "ID-2"
