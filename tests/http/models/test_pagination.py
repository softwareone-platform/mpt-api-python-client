import pytest

from mpt_api_client.http.models import Pagination


class TestPagination:  # noqa: WPS214
    def test_default_page(self):  # noqa: WPS218
        pagination = Pagination()

        assert pagination.limit == 0
        assert pagination.offset == 0
        assert pagination.total == 0

        assert pagination.has_next() is False
        assert pagination.num_page() == 0
        assert pagination.total_pages() == 0
        assert pagination.next_offset() == 0

    def test_pagination_initialization(self):
        pagination = Pagination(limit=10, offset=0, total=100)

        assert pagination.limit == 10
        assert pagination.offset == 0
        assert pagination.total == 100

    def test_has_next_with_more_items(self):
        pagination = Pagination(limit=10, offset=0, total=100)

        assert pagination.has_next() is True

    def test_has_next_with_no_more_items(self):
        pagination = Pagination(limit=10, offset=90, total=100)

        assert pagination.has_next() is False

    def test_has_next_exact_boundary(self):
        pagination = Pagination(limit=25, offset=75, total=100)

        assert pagination.has_next() is False

    def test_num_page_first_page(self):
        pagination = Pagination(limit=10, offset=0, total=100)

        assert pagination.num_page() == 1

    def test_num_page_middle_page(self):
        pagination = Pagination(limit=10, offset=20, total=100)

        assert pagination.num_page() == 3

    def test_num_page_last_page(self):
        pagination = Pagination(limit=10, offset=90, total=100)

        assert pagination.num_page() == 10

    def test_total_pages_even_division(self):
        pagination = Pagination(limit=10, offset=0, total=100)

        assert pagination.total_pages() == 10

    def test_total_pages_with_remainder(self):
        pagination = Pagination(limit=10, offset=0, total=95)

        assert pagination.total_pages() == 10

    def test_total_pages_single_item(self):
        pagination = Pagination(limit=10, offset=0, total=1)

        assert pagination.total_pages() == 1

    def test_total_pages_empty(self):
        pagination = Pagination(limit=10, offset=0, total=0)

        assert pagination.total_pages() == 0

    def test_next_offset_calculation(self):
        pagination = Pagination(limit=25, offset=50, total=200)

        assert pagination.next_offset() == 75

    def test_next_offset_from_start(self):
        pagination = Pagination(limit=10, offset=0, total=100)

        assert pagination.next_offset() == 10

    @pytest.mark.parametrize(
        ("limit", "offset", "total", "expected_has_next"),
        [
            (10, 0, 50, True),
            (10, 40, 50, False),
            (20, 0, 20, False),
            (5, 45, 50, False),
            (15, 30, 50, True),
        ],
    )
    def test_has_next_parametrized(self, limit, offset, total, expected_has_next):
        pagination = Pagination(limit=limit, offset=offset, total=total)

        assert pagination.has_next() == expected_has_next

    @pytest.mark.parametrize(
        ("limit", "offset", "expected_page"),
        [
            (10, 0, 1),
            (10, 10, 2),
            (10, 25, 3),
            (20, 40, 3),
            (5, 47, 10),
        ],
    )
    def test_num_page_parametrized(self, limit, offset, expected_page):
        pagination = Pagination(limit=limit, offset=offset, total=100)

        assert pagination.num_page() == expected_page
