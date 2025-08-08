from httpx import Response

from mpt_api_client.models.collection import Collection
from mpt_api_client.models.resource import Resource


class ChargeResourceMock(Collection[Resource]):
    _data_key = "charge"


def charge(charge_id, amount) -> dict[str, int]:
    return {"id": charge_id, "amount": amount}


def test_custom_data_key():
    payload = {"charge": [charge(1, 100), charge(2, 101)]}
    response = Response(200, json=payload)

    resource = ChargeResourceMock.from_response(response)

    assert resource[0].to_dict() == charge(1, 100)
