from httpx import Response

from mpt_api_client.models import Resource


class ChargeResourceMock(Resource):
    _data_key = "charge"


def test_custom_data_key():
    record_data = {"id": 1, "amount": 100}
    response = Response(200, json={"charge": record_data})

    resource = ChargeResourceMock.from_response(response)

    assert resource.id == 1
    assert resource.amount == 100
