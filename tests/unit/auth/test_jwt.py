import base64
import json

import pytest

from mpt_api_client.auth.jwt import (
    JWTClaimsError,
    JWTFormatError,
    decode_unverified_jwt_claims,
)


def _encode_segment(payload: object) -> str:
    raw = json.dumps(payload).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")


def _build_jwt(claims: dict) -> str:
    return f"{_encode_segment({'alg': 'none'})}.{_encode_segment(claims)}.signature"


def test_decode_valid_jwt_returns_claims():
    token = _build_jwt({"exp": 1234567890, "sub": "user"})

    claims = decode_unverified_jwt_claims(token)  # act

    assert claims == {"exp": 1234567890, "sub": "user"}


def test_decode_rejects_token_without_three_parts():
    with pytest.raises(JWTFormatError):  # act
        decode_unverified_jwt_claims("not.a-jwt")


def test_decode_rejects_invalid_base64_payload():
    token = "header.!!!not-base64!!!.signature"

    with pytest.raises(JWTClaimsError):  # act
        decode_unverified_jwt_claims(token)


def test_decode_rejects_non_dict_claims():
    header_segment = _encode_segment({"alg": "none"})
    payload_segment = _encode_segment([1, 2, 3])
    token = f"{header_segment}.{payload_segment}.signature"

    with pytest.raises(JWTClaimsError):  # act
        decode_unverified_jwt_claims(token)
