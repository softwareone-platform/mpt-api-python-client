import pytest

from mpt_api_client.http.client_utils import validate_base_url


@pytest.mark.parametrize(
    ("input_url", "expected"),
    [
        ("//[2001:db8:85a3::8a2e:370:7334]:80/a", "https://[2001:db8:85a3::8a2e:370:7334]:80/a"),
        ("//example.com", "https://example.com"),
        ("http://example.com", "http://example.com"),
        ("http://example.com:88/something/else", "http://example.com:88/something/else"),
        ("http://user@example.com:88/", "http://example.com:88"),
        ("http://user:pass@example.com:88/", "http://example.com:88"),
        ("http://example.com/public", "http://example.com"),
        ("http://example.com/public/", "http://example.com"),
        ("http://example.com/public/else", "http://example.com/public/else"),
        ("http://example.com/public/v1", "http://example.com"),
        ("http://example.com/public/v1/", "http://example.com"),
        ("http://example.com/else/public", "http://example.com/else/public"),
        ("http://example.com/elsepublic", "http://example.com/elsepublic"),
    ],
)
def test_protocol_and_host(input_url, expected):
    result = validate_base_url(input_url)

    assert result == expected


@pytest.mark.parametrize(
    "input_url",
    [
        "",
        "http//example.com",
        "://example.com",
        "http:example.com",
        "http:/example.com",
    ],
)
def test_protocol_and_host_error(input_url):
    with pytest.raises(ValueError):
        validate_base_url(input_url)
