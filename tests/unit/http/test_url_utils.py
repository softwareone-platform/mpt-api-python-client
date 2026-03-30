import pytest

from mpt_api_client.http.url_utils import join_url_path


def test_simple_segment():
    result = join_url_path("/api/v1/orders", "ORD-001")

    assert result == "/api/v1/orders/ORD-001"


def test_multiple_segments():
    result = join_url_path("/api/v1/orders", "ORD-001", "complete")

    assert result == "/api/v1/orders/ORD-001/complete"


def test_base_with_trailing_slash():
    result = join_url_path("/api/v1/orders/", "ORD-001")

    assert result == "/api/v1/orders/ORD-001"


def test_segment_with_leading_slash():
    result = join_url_path("/api/v1/orders", "/ORD-001")

    assert result == "/api/v1/orders/ORD-001"


def test_segment_with_surrounding_slashes():
    result = join_url_path("/api/v1/orders/", "/ORD-001/")

    assert result == "/api/v1/orders/ORD-001"


def test_absolute_segment():
    result = join_url_path("/api/v1/orders", "https://evil.com")

    assert result == "/api/v1/orders/https://evil.com"


def test_dotdot_segment_is_literal():
    result = join_url_path("/api/v1/orders", "../other")

    assert result == "/api/v1/orders/../other"


def test_no_segments():
    result = join_url_path("/api/v1/orders")

    assert result == "/api/v1/orders"


def test_empty_segment_is_skipped():
    result = join_url_path("/api/v1/orders", "", "upload")

    assert result == "/api/v1/orders/upload"


def test_none_segment_is_skipped():
    result = join_url_path("/api/v1/orders", None, "upload")  # type: ignore[arg-type]

    assert result == "/api/v1/orders/upload"


@pytest.mark.parametrize(
    ("base", "segments", "expected"),
    [
        ("/public/v1/billing/journals", ("JRN-123",), "/public/v1/billing/journals/JRN-123"),
        (
            "/public/v1/billing/journals",
            ("JRN-123", "upload"),
            "/public/v1/billing/journals/JRN-123/upload",
        ),
        (
            "/public/v1/billing/custom-ledgers",
            ("CL-456", "upload"),
            "/public/v1/billing/custom-ledgers/CL-456/upload",
        ),
    ],
    ids=["resource-id", "resource-id-and-action", "custom-ledger-upload"],
)
def test_real_world_paths(base, segments, expected):
    result = join_url_path(base, *segments)

    assert result == expected
