import pytest

from mpt_api_client.models import Pagination


def test_default_page():  # noqa: WPS218
    result = Pagination()

    assert result.limit == 0
    assert result.offset == 0
    assert result.total == 0
    assert result.has_next() is False
    assert result.num_page() == 0
    assert result.total_pages() == 0
    assert result.next_offset() == 0


def test_pagination_initialization():
    result = Pagination(limit=10, offset=0, total=100)

    assert result.limit == 10
    assert result.offset == 0
    assert result.total == 100


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

    result = pagination.has_next()

    assert result == expected_has_next


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

    result = pagination.num_page()

    assert result == expected_page


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

    result = pagination.total_pages()

    assert result == expected_total_pages


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

    result = pagination.next_offset()

    assert result == expected_next_offset
