import pytest

from mpt_api_client.models import Pagination


def test_default_page():  # noqa: WPS218
    pagination = Pagination()

    assert pagination.limit == 0
    assert pagination.offset == 0
    assert pagination.total == 0

    assert pagination.has_next() is False
    assert pagination.num_page() == 0
    assert pagination.total_pages() == 0
    assert pagination.next_offset() == 0


def test_pagination_initialization():
    pagination = Pagination(limit=10, offset=0, total=100)

    assert pagination.limit == 10
    assert pagination.offset == 0
    assert pagination.total == 100


@pytest.mark.parametrize(
    ("num_page", "total_pages", "expected_has_next"),
    [
        (0, 0, False),
        (1, 100, True),
        (100, 1, False),
    ],
)
def test_has_next(mocker, num_page, total_pages, expected_has_next):
    pagination = Pagination()
    mocker.patch.object(pagination, "num_page", return_value=num_page)
    mocker.patch.object(pagination, "total_pages", return_value=total_pages)

    has_next = pagination.has_next()

    assert has_next == expected_has_next


@pytest.mark.parametrize(
    ("limit", "offset", "expected_page"),
    [
        (0, 0, 0),
        (1, 0, 0),
        (5, 5, 1),
        (10, 990, 99),
        (245, 238, 0),
    ],
)
def test_num_page(limit, offset, expected_page):
    pagination = Pagination(limit=limit, offset=offset, total=5)

    assert pagination.num_page() == expected_page


@pytest.mark.parametrize(
    ("limit", "total", "expected_total_pages"),
    [
        (0, 0, 0),
        (0, 2, 0),
        (1, 1, 1),
        (1, 2, 2),
    ],
)
def test_total_pages(limit, total, expected_total_pages):
    pagination = Pagination(limit=limit, offset=0, total=total)

    assert pagination.total_pages() == expected_total_pages


@pytest.mark.parametrize(
    ("limit", "offset", "expected_next_offset"),
    [
        (0, 0, 0),
        (1, 0, 1),
        (1, 2, 3),
    ],
)
def test_next_offset(limit, offset, expected_next_offset):
    pagination = Pagination(limit=limit, offset=offset, total=3)

    assert pagination.next_offset() == expected_next_offset
