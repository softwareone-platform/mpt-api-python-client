from httpx import Response

from mpt_api_client.models import Model


class ChargeResourceMock(Model):
    _data_key = "charge"


def test_custom_data_key():
    record_data = {"id": 1, "amount": 100}
    response = Response(200, json={"charge": record_data})

    result = ChargeResourceMock.from_response(response)

    assert result.id == "1"
    assert result.amount == 100
