import pytest

from mpt_api_client.http.client_utils import get_query_params, validate_base_url
from mpt_api_client.http.query_options import QueryOptions


@pytest.mark.parametrize(
    ("query_params", "options", "expected"),
    [
        (None, None, ""),
        ({}, None, ""),
        ({"select": None}, None, ""),
        ({"select": "id,name"}, None, "select=id%2Cname"),
        ({"select": "id", "order": "asc"}, None, "select=id&order=asc"),
        (None, QueryOptions(render=True), "render()"),
        ({}, QueryOptions(render=True), "render()"),
        ({"select": "id"}, QueryOptions(render=True), "select=id&render()"),
        ({"select": None}, QueryOptions(render=True), "render()"),
        (None, QueryOptions(render=False), ""),
        (None, QueryOptions(metadata=True), "metadata"),
        ({}, QueryOptions(metadata=True), "metadata"),
        ({"select": "id"}, QueryOptions(metadata=True), "select=id&metadata"),
        ({"select": None}, QueryOptions(metadata=True), "metadata"),
        (None, QueryOptions(metadata=False), ""),
    ],
)
def test_get_query_params(query_params, options, expected):
    result = get_query_params(query_params, options)

    assert result == expected


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
