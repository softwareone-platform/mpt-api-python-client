import httpx
import pytest


@pytest.fixture
def single_page_response():
    return httpx.Response(
        httpx.codes.OK,
        json={
            "data": [
                {"id": "ID-1", "name": "Resource 1"},
                {"id": "ID-2", "name": "Resource 2"},
            ],
            "$meta": {
                "pagination": {
                    "total": 2,
                    "offset": 0,
                    "limit": 100,
                }
            },
        },
    )


@pytest.fixture
def multi_page_response_page1():
    return httpx.Response(
        httpx.codes.OK,
        json={
            "data": [
                {"id": "ID-1", "name": "Resource 1"},
                {"id": "ID-2", "name": "Resource 2"},
            ],
            "$meta": {
                "pagination": {
                    "total": 4,
                    "offset": 0,
                    "limit": 2,
                }
            },
        },
    )


@pytest.fixture
def multi_page_response_page2():
    return httpx.Response(
        httpx.codes.OK,
        json={
            "data": [
                {"id": "ID-3", "name": "Resource 3"},
                {"id": "ID-4", "name": "Resource 4"},
            ],
            "$meta": {
                "pagination": {
                    "total": 4,
                    "offset": 2,
                    "limit": 2,
                }
            },
        },
    )


@pytest.fixture
def empty_response():
    return httpx.Response(
        httpx.codes.OK,
        json={
            "data": [],
            "$meta": {
                "pagination": {
                    "total": 0,
                    "offset": 0,
                    "limit": 100,
                }
            },
        },
    )


@pytest.fixture
def no_meta_response():
    return httpx.Response(
        httpx.codes.OK,
        json={
            "data": [
                {"id": "ID-1", "name": "Resource 1"},
                {"id": "ID-2", "name": "Resource 2"},
            ]
        },
    )
